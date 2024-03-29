from __future__ import annotations

from collections import defaultdict, namedtuple
from dataclasses import dataclass
from datetime import datetime, timedelta
from functools import lru_cache, partial, reduce, singledispatch
from itertools import count, dropwhile
from typing import (
    Any,
    Callable,
    Dict,
    Generator,
    Iterable,
    Iterator,
    List,
    NewType,
    Optional,
    Set,
    Tuple,
    Union,
    cast,
    overload,
)

import geopy.distance as gpd
import numpy as np
import pandas as pd
import shapely.geometry as sg
from shapely.geometry import LineString, Point

import busboy.apis as api
import busboy.constants as c
import busboy.database as db
import busboy.model as m
import busboy.util as u
from busboy.geo import Latitude, Longitude, to_metre_point
from busboy.util import Just, Maybe, Nothing, drop, first, pairwise, tuplewise_padded

Coord = Tuple[Latitude, Longitude]
DistanceVector = NewType("DistanceVector", Tuple[float, float])


def pd_stop_distance(r: Any, stop: Coord) -> float:
    return gpd.distance(stop, (r.latitude, r.longitude)).m


def pd_stop_distances(df: pd.DataFrame, stop: Coord) -> pd.DataFrame:
    df2 = df.copy()
    df2["stop_distance"] = [pd_stop_distance(r, stop) for r in df.itertuples()]
    return df2


def stop_times_220(df: pd.DataFrame) -> pd.DataFrame:
    """Given the dataframe for a 220 trip, work out the times it reached each stop."""
    dfs = []
    for s in c.stops_on_220:
        if s is not None:
            ndf = pd_stop_distances(df, (s.latitude, s.longitude))
            ndf = ndf[ndf["stop_distance"] < 100]
            include_stop(ndf, s)
            dfs.append(ndf)
    return pd.concat(dfs)


def closest_stops_220(df: pd.DataFrame) -> pd.DataFrame:
    """Given the dataframe for a 220 trip, work out the closest stop for the bus at each point."""
    df["closest_stop"] = [
        closest_stop_gpd(r.latitude, r.longitude, c.stops_on_220)
        for r in df.itertuples()
    ]
    return df


def closest_stop_gpd(latitude: float, longitude: float, stops: List[m.Stop]) -> m.Stop:
    return min(
        stops,
        key=lambda s: gpd.distance((s.latitude, s.longitude), (latitude, longitude)),
    )


def include_stop(df: pd.DataFrame, s: m.Stop) -> pd.DataFrame:
    df["stop_id"] = s.id
    df["stop_name"] = s.name
    return df


def new_stop_distance(e: db.BusSnapshot, s: m.Stop) -> float:
    return gpd.distance((e.latitude, e.longitude), (s.latitude, s.longitude))


def new_stop_distances(es: List[db.BusSnapshot], s: m.Stop) -> List[float]:
    return [new_stop_distance(e, s) for e in es]


def distance_vector(c1: Coord, c2: Coord) -> DistanceVector:
    """A naive cartesian distance vector between two lon-lat coordinates in metres."""
    mid = (c2[0], c1[1])
    abs_x = gpd.distance(c1, mid).m
    abs_y = gpd.distance(mid, c2).m
    if c2[0] >= c1[0]:
        x = abs_x
    else:
        x = -abs_x
    if c2[1] >= c1[1]:
        y = abs_y
    else:
        y = -abs_y
    return cast(DistanceVector, (x, y))


def unit_vector(vector):
    """The unit vector of a vector.

    From: https://stackoverflow.com/questions/2827393/angles-between-two-n-dimensional-vectors-in-python#13849249
    """
    return vector / np.linalg.norm(vector)


def angle_between(v1: DistanceVector, v2: DistanceVector) -> float:
    """The angle in radians between two vectors.

    From: https://stackoverflow.com/questions/2827393/angles-between-two-n-dimensional-vectors-in-python#13849249
    """
    v1_u = unit_vector(v1)
    v2_u = unit_vector(v2)
    return np.arccos(np.clip(np.dot(v1_u, v2_u), -1.0, 1.0))


RouteSection = Union["RoadSection", "StopCircle"]


@lru_cache(maxsize=2 ** 24)
def cached_contains(polygon: sg.Polygon, lon: Longitude, lat: Latitude) -> bool:
    return polygon.contains(Point(lat, lon))


@dataclass(frozen=True)
class AbstractRouteSection(object):
    polygon: sg.Polygon

    def contains(self, lon: Longitude, lat: Latitude) -> bool:
        return cached_contains(self.polygon, lon, lat)


@dataclass(frozen=True)
class RoadSection(AbstractRouteSection):
    def difference(self, circle: StopCircle) -> Maybe[RoadSection]:
        new_polygon = self.polygon.difference(circle.polygon)
        if isinstance(new_polygon, sg.Polygon):
            return Just(RoadSection(monkey_patch_polygon(new_polygon)))
        else:
            return Nothing()


@dataclass(frozen=True)
class StopCircle(AbstractRouteSection):
    stop: m.Stop


def hash_polygon(polygon: sg.Polygon) -> int:
    """polygon should be a monkey-patched Polygon"""
    return polygon._busboy_id  # type:ignore


polygon_ids = count()
sg.Polygon.__hash__ = hash_polygon  # type: ignore


def monkey_patch_polygon(polygon: sg.Polygon) -> sg.Polygon:
    polygon._busboy_id = next(polygon_ids)  # type:ignore
    return polygon


@lru_cache(maxsize=4096)
def make_circle(stop: m.Stop, circle_radius: float) -> StopCircle:
    return StopCircle(
        monkey_patch_polygon(
            cast(sg.Polygon, sg.Point(stop.lat_lon).buffer(circle_radius))
        ),
        stop,
    )


@lru_cache(maxsize=4096)
def make_rectangle(s1: m.Stop, s2: m.Stop, rectangle_width: float) -> RoadSection:
    return RoadSection(
        monkey_patch_polygon(
            widen_line(
                cast(
                    LineString,
                    sg.MultiPoint([s1.lat_lon, s2.lat_lon]).minimum_rotated_rectangle,
                ),
                rectangle_width,
            )
        )
    )


def route_sections(
    stops: Iterable[m.Stop],
    rectangle_width: float = 0.001,
    circle_radius: float = 0.001,
) -> Iterator[RouteSection]:
    def shapes() -> Iterator[RouteSection]:
        for s1, s2 in pairwise(stops):
            yield make_circle(s1, circle_radius)
            yield make_rectangle(s1, s2, rectangle_width)
        yield make_circle(s2, circle_radius)

    for section1, section2, section3 in drop(
        1, (tuplewise_padded(3, (Just(x) for x in shapes()), pad_value=Nothing()))
    ):
        if isinstance(section2, Just):
            if isinstance(section2.value, RoadSection):
                if isinstance(section1, Just) and isinstance(
                    section1.value, StopCircle
                ):
                    section2 = section2.value.difference(section1.value)
                if isinstance(section3, Just) and isinstance(
                    section3.value, StopCircle
                ):
                    section2 = section2.bind(lambda s: s.difference(section3.value))
        if isinstance(section2, Just):
            yield section2.value


def widen_line(linestring: sg.LineString, width: float) -> sg.Polygon:
    linestrings = [
        linestring,
        linestring.parallel_offset(width, "left"),
        linestring.parallel_offset(width, "right"),
    ]
    return sg.MultiLineString(linestrings).minimum_rotated_rectangle


def assign_region(
    sections: Iterable[RouteSection], e: db.BusSnapshot
) -> Tuple[db.BusSnapshot, List[RouteSection]]:
    return (e, [s for s in sections if s.polygon.contains(e.point)])


def assign_regions(
    rs: Iterable[RouteSection], es: Iterable[db.BusSnapshot]
) -> Generator[Tuple[db.BusSnapshot, List[RouteSection]], None, None]:
    return (assign_region(rs, e) for e in es)


def most_recent_stops(
    ts: Iterable[Tuple[db.BusSnapshot, List[RouteSection]]]
) -> Iterable[Tuple[db.BusSnapshot, Maybe[m.Stop]]]:
    def choose_stop(rs: List[RouteSection]) -> Maybe[m.Stop]:
        if len(rs) == 0:
            return Nothing()
        elif len(rs) == 1:
            return Just(rs[0].s1)
        elif rs[0].s2 == rs[1].s1:
            return Just(rs[0].s2)
        else:
            return Just(rs[0].s1)

    return ((e, choose_stop(rs)) for e, rs in ts)


def possible_variants(
    snapshots: Iterable[db.BusSnapshot],
    sections: Dict[api.TimetableVariant, List[RouteSection]],
) -> Iterable[Tuple[db.BusSnapshot, Set[Tuple[api.TimetableVariant, int]]]]:
    for snapshot in snapshots:
        positions = []
        for tv, rs in sections.items():
            for i, section in enumerate(rs):
                if section.contains(snapshot.longitude, snapshot.latitude):
                    positions.append((tv, i))
        yield (snapshot, set(positions))


def check_variant_order(
    snapshots: List[Tuple[db.BusSnapshot, Set[Tuple[api.TimetableVariant, int]]]]
) -> Iterable[Tuple[db.BusSnapshot, Set[Tuple[api.TimetableVariant, int]]]]:
    for i, (snapshot, positions) in enumerate(snapshots):
        output_positions: Set[Tuple[api.TimetableVariant, int]] = set()
        for variant, position in positions:
            later_positions = map(lambda j: snapshots[j][1], range(i, len(snapshots)))
            first_change_positions = dict(
                first(
                    dropwhile(
                        lambda ps: len(ps) == 0 or (variant, position) in ps,
                        later_positions,
                    )
                ).or_else([])
            )
            if (
                variant in first_change_positions
                and first_change_positions[variant] > position
            ):
                output_positions.add((variant, position))
        yield (snapshot, output_positions)


def duplicate_positions(s1: db.BusSnapshot, s2: db.BusSnapshot) -> bool:
    return (s1.poll_time, s1.latitude, s1.longitude) == (
        s2.poll_time,
        s2.latitude,
        s2.longitude,
    )


def drop_duplicate_positions(
    snapshots: Iterable[db.BusSnapshot],
    duplicates: Callable[[db.BusSnapshot, db.BusSnapshot], bool] = duplicate_positions,
) -> Iterator[db.BusSnapshot]:
    last = None
    for this in snapshots:
        if last is None or not duplicates(last, this):
            yield this
        last = this


EntryWindow = Tuple[Maybe[datetime], Maybe[datetime]]
ExitWindow = Tuple[Maybe[datetime], Maybe[datetime]]
SectionTime = NewType("SectionTime", Tuple[int, EntryWindow, ExitWindow])


def section_times(
    snapshots: List[Tuple[db.BusSnapshot, Dict[api.TimetableVariant, Set[int]]]],
    sections: Dict[api.TimetableVariant, List[RouteSection]],
) -> Dict[api.TimetableVariant, List[SectionTime]]:
    """Calculates entry and exit times for each section in snapshots.

    Arguments:
        snapshots: The bus snapshots, each with, for each timetable variant,
            the sections that snapshot falls in.
        sections: The sections in each timetable variant (in order).

    Returns:
        For each timetable variant, the route sections that were entered and
        exited in snapshots, in order of exit.
    """
    section_windows: Dict[api.TimetableVariant, List[SectionTime]] = defaultdict(list)
    sections_entered: Dict[Tuple[api.TimetableVariant, int], EntryWindow] = {}
    last_positions: Dict[api.TimetableVariant, Set[int]] = {}
    last_time: Maybe[datetime] = Nothing()
    for snapshot, positions in snapshots:
        update_positions = False
        for variant, these_positions in positions.items():
            if not these_positions:
                continue
            else:
                update_positions = True
            for position in these_positions.difference(
                last_positions.get(variant, set())
            ):
                window = (last_time, Just(snapshot.poll_time))
                sections_entered[(variant, position)] = window
            for position in last_positions.get(variant, set()).difference(
                these_positions
            ):
                exit_interval = last_time, Just(snapshot.poll_time)
                section_time = SectionTime(
                    (position, sections_entered[(variant, position)], exit_interval)
                )
                section_windows[variant].append(section_time)
        for variant, old_positions in last_positions.items():
            if variant not in positions:
                for position in list(old_positions):
                    exit_interval = last_time, Just(snapshot.poll_time)
                    section_time = SectionTime(
                        (position, sections_entered[(variant, position)], exit_interval)
                    )
                    section_windows[variant].append(section_time)
                    old_positions.remove(position)
        if update_positions:
            last_positions = positions
            last_time = Just(snapshot.poll_time)
    return section_windows


def journeys(
    section_times: Dict[api.TimetableVariant, List[SectionTime]]
) -> Dict[api.TimetableVariant, List[List[SectionTime]]]:
    """Splits a vehicle’s positions on a timetable into journeys from start to
    end.
    """
    Accumulator = NewType(
        "Accumulator", Tuple[int, List[SectionTime], List[List[SectionTime]]]
    )

    def f(acc: Accumulator, x: SectionTime) -> Accumulator:
        position, _, _ = x
        last_position, this_journey, journeys = acc
        if position < last_position:
            return Accumulator((position, [x], journeys + [this_journey]))
        else:
            return Accumulator((position, this_journey + [x], journeys))

    output = {}
    for v, ts in section_times.items():
        reduced = reduce(f, ts, Accumulator((0, [], [])))
        output[v] = reduced[2] + [reduced[1]]
    return output
    # journeys = []
    # this_journey: List[Tuple[int, EntryWindow, ExitWindow]] = []
    # last_position = 0
    # for position, entry, exit in times:
    #     if position < last_position:
    #         journeys.append(this_journey)
    #         this_journey = []
    #     this_journey.append((position, entry, exit))
    #     last_position = position
    # output[variant] = journeys


def pad_journeys(
    variant_journeys: Dict[api.TimetableVariant, List[List[SectionTime]]]
) -> Dict[api.TimetableVariant, List[List[SectionTime]]]:
    """Fill in missing sections in journeys."""
    output = {}
    for variant, journeys in variant_journeys.items():
        output_journeys = []
        for journey in journeys:
            output_journey: List[SectionTime] = []
            last_position = -1
            last_exit: ExitWindow = (Nothing(), Nothing())
            for time in journey:
                position, entry, exit = time
                for missing_position in range(last_position + 1, position):
                    output_journey.append(
                        SectionTime(
                            (
                                missing_position,
                                (last_exit[0], Nothing()),
                                (Nothing(), last_exit[1]),
                            )
                        )
                    )
                output_journey.append(time)
                last_position = position
                last_exit = exit
            output_journeys.append(output_journey)
        output[variant] = output_journeys
    return output


StopArrival = Union["SeenAtStop", "NotSeenAtStop"]


@dataclass
class SeenAtStop(object):
    last_before: Maybe[datetime]
    first_at: datetime
    last_at: datetime
    first_after: Maybe[datetime]


@dataclass
class NotSeenAtStop(object):
    last_before: Maybe[datetime]
    first_after: Maybe[datetime]


def stop_times(
    snapshots: List[Tuple[db.BusSnapshot, Dict[api.TimetableVariant, Set[int]]]],
    sections: Dict[api.TimetableVariant, List[RouteSection]],
) -> Dict[api.TimetableVariant, List[List[StopArrival]]]:
    """Calculate time windows in which a bus reached each stop on its route."""
    section_windows: Dict[api.TimetableVariant, List[List[SectionTime]]] = pad_journeys(
        journeys(section_times(snapshots, sections))
    )
    output: Dict[api.TimetableVariant, List[List[StopArrival]]] = {}
    for variant, variant_journeys in section_windows.items():
        journey_stops = []
        for journey in variant_journeys:
            stops: List[StopArrival] = []
            for position, entry, exit in journey:
                if isinstance(sections[variant][position], StopCircle):
                    if isinstance(entry[1], Just) and isinstance(exit[0], Just):
                        stops.append(
                            SeenAtStop(entry[0], entry[1].value, exit[0].value, exit[1])
                        )
                    else:
                        stops.append(NotSeenAtStop(entry[0], exit[1]))
            journey_stops.append(stops)
        output[variant] = journey_stops
    return output


def journeys_dataframe(
    journeys: Iterable[
        Tuple[api.TimetableVariant, List[List[Optional[Tuple[datetime, datetime]]]]]
    ]
) -> Iterator[Tuple[api.TimetableVariant, pd.DataFrame]]:
    for variant, js in journeys:
        data: Dict[str, List[Optional[datetime]]] = {}
        for stop in variant.stops:
            data[f"{stop.name} [arrival]"] = []
            data[f"{stop.name} [departure]"] = []
        for journey in js:
            for position, stop in enumerate(variant.stops):
                time = journey[position] if position < len(journey) else None
                if time is None:
                    arrival_time = None
                    departure_time = None
                else:
                    arrival_time, departure_time = time
                data[f"{stop.name} [arrival]"].append(arrival_time)
                data[f"{stop.name} [departure]"].append(departure_time)
        yield (variant, pd.DataFrame(data))


def estimate_arrival(
    variant_journeys: Iterable[Tuple[api.TimetableVariant, List[List[StopArrival]]]]
) -> Iterator[
    Tuple[api.TimetableVariant, List[List[Optional[Tuple[datetime, datetime]]]]]
]:
    def estimate(arrival: StopArrival) -> Maybe[Tuple[datetime, datetime]]:
        if isinstance(arrival, SeenAtStop):
            return Just((arrival.first_at, arrival.last_at))
        elif isinstance(arrival, NotSeenAtStop):
            return arrival.last_before.bind(
                lambda before: arrival.first_after.map(
                    lambda after: before + ((after - before) / 2)
                ).map(lambda a: (a, a))
            )

    for variant, journeys in variant_journeys:
        new_journeys = [[estimate(a).or_else(None) for a in j] for j in journeys]
        yield (variant, new_journeys)


def stop_times_proximity(
    snapshots: Iterable[db.BusSnapshot],
    stops: Iterable[m.Stop],
    distance_limit: float = 100,
) -> Iterator[Tuple[m.Stop, datetime]]:
    for snapshot in snapshots:
        for stop in stops:
            distance = stop_distance_geopandas(snapshot, stop)
            if distance < distance_limit:
                yield (stop, snapshot.poll_time)


def stop_distance_geopandas(snapshot: db.BusSnapshot, stop: m.Stop) -> float:
    snapshot_point = to_metre_point((snapshot.longitude, snapshot.latitude))
    stop_point = to_metre_point((stop.longitude, stop.latitude))
    return snapshot_point.distance(stop_point)
