import traceback
import warnings
from collections import deque
from datetime import datetime, time, timedelta
from pathlib import Path
from sys import argv
from time import sleep
from typing import Any, Callable, Deque, Dict, List, Optional, Set, Union

import pandas as pd
from pandas import DataFrame
from sklearn.dummy import DummyRegressor

import busboy.database as db
import busboy.prediction as prediction
from busboy.apis import stop_passage
from busboy.constants import example_stops
from busboy.database import BusSnapshot, default_connection, stop_by_id
from busboy.geo import DegreeLatitude, DegreeLongitude
from busboy.model import Passage, PassageId, RouteId, StopId, VehicleId
from busboy.prediction import RouteSection
from busboy.prediction.pandas import travel_times
from busboy.prediction.sklearn import journeys as separate_journeys
from busboy.util import Just, Maybe, Right, pairwise
from busboy.util.notebooks import read_preprocessed_data


def main() -> None:
    stops = {
        "opposite wgb": StopId("7338653551721425381"),
        "wgb": StopId("7338653551721425841"),
        "ballincollig supervalu": StopId("7338653551721543021"),
        "ballincollig aylsbury": StopId("7338653551721429511"),
        "church cross east": example_stops["cce"].id,
        "church cross west": example_stops["ccw"].id,
        "grand parade caseys": example_stops["gpc"].id,
        "ovens": example_stops["ovens"].id,
        "ovens grange road": StopId("7338653551722184832"),
        "carrigaline": StopId("7338653551721431991"),
    }
    live_test(stops[" ".join(argv[1:])])


def live_test(stop_id: StopId) -> None:
    pd.set_option("display.max_rows", 1_000_000_000)
    pd.set_option("display.max_columns", 1_000_000_000)
    pd.set_option("display.width", 1_000_000_000)
    warnings.simplefilter("ignore")
    stop = stop_by_id(default_connection(), stop_id).value
    routes_by_id = db.routes_by_id()
    routes_by_name = db.routes_by_name()
    timetables = [
        tt.value
        for tt in db.timetables(routes_by_name["220"].id)
        if isinstance(tt, Right)
    ]
    variants = {v for timetable in timetables for v in timetable.variants}
    filtered_variants = {v for v in variants if stop in v.stops}
    timetable = sorted(filtered_variants, key=lambda v: len(v.stops))[-1]
    route_sections = list(prediction.route_sections(timetable.stops))
    snapshots: Dict[VehicleId, List[BusSnapshot]] = {}
    print("Training predictors…")
    preprocessed_by_timetable = dict(read_preprocessed_data("220"))
    preprocessed = preprocessed_by_timetable[timetable]
    bins = [time(i) for i in range(23)] + [time(23, 59, 59, 999_999)]
    average_predictors = train_average_predictors(
        preprocessed, stop.name + " [arrival]"
    )
    binned_predictors = train_binned_average_predictors(
        preprocessed, stop.name + " [arrival]", bins
    )
    day_binned_predictors = train_day_binned_predictors(
        preprocessed, stop.name + " [arrival]", bins
    )
    print("Finished training.")
    responses: Deque[DataFrame] = deque(maxlen=720)
    arrived_passages: Dict[PassageId, datetime] = {}
    stats_output_file = Path(
        f"/Users/Noel/Developer/Projects/Busboy/data/live/{stop.name}-{datetime.now().date().isoformat()}.csv"
    )
    while True:
        try:
            print("-" * 80)
            loop_start = datetime.now()
            response = (
                stop_passage(stop.id, timeout=5)
                .dataframe()
                .sort_values("scheduled_arrival")
            )
            response["poll_time"] = loop_start
            response = response[
                response["predicted_arrival"] > loop_start - timedelta(minutes=10)
            ]
            response["route"] = response["route"].apply(
                lambda r: Maybe.of(routes_by_id.get(RouteId(r)))
                .map(lambda r: r.name)
                .or_else(None)
            )
            response = response[response["route"] == "220"]
            response["sections"] = [
                containing_sections(route_sections, r.longitude, r.latitude)
                for r in response.itertuples()
            ]
            arrived = [
                arrived_passages.get(p.id.value, pd.NaT) for p in response["passage"]
            ]
            my_predictions = [pd.NaT] * len(response["passage"])
            binned_predictions = [pd.NaT] * len(response["passage"])
            response["day_binned_prediction"] = pd.NaT
            last_stops = [None] * len(response["passage"])
            for row, passage in enumerate(response["passage"]):
                if isinstance(passage.vehicle, Just):
                    snapshot = BusSnapshot.from_passage(passage, loop_start)
                    snapshots.setdefault(passage.vehicle.value, []).append(snapshot)
                    timetable_journeys = separate_journeys(
                        snapshots[passage.vehicle.value],
                        {timetable},
                        {timetable: route_sections},
                    )
                    journeys = timetable_journeys.get(timetable)
                    if journeys is not None:
                        journeys = journeys.fillna(value=pd.NaT)
                        nonempty = journeys.loc[:, journeys.notna().any()]
                        if len(nonempty.columns) > 0:
                            last = nonempty.columns[-1]
                            last_stops[row] = last
                            if last in average_predictors:
                                predicted_travel_time = average_predictors[
                                    last
                                ].predict(journeys)
                                predicted_arrival = journeys[last].iloc[-1] + timedelta(
                                    seconds=predicted_travel_time[-1]
                                )
                                my_predictions[row] = predicted_arrival
                            binned_predictor = binned_predictors(
                                last, loop_start.time()
                            )  # should be last_time
                            if binned_predictor is not None:
                                predicted_travel_time = binned_predictor.predict(
                                    journeys
                                )
                                predicted_arrival = journeys[last].iloc[-1] + timedelta(
                                    seconds=predicted_travel_time[-1]
                                )
                                binned_predictions[row] = predicted_arrival
                            day_binned_predictor = day_binned_predictors(
                                last, loop_start
                            )  # should be last_day
                            if day_binned_predictor is not None:
                                predicted_travel_time = day_binned_predictor.predict(
                                    journeys
                                )
                                predicted_arrival = journeys[last].iloc[-1] + timedelta(
                                    seconds=predicted_travel_time[-1]
                                )
                                if not pd.isnull(predicted_arrival):
                                    response["day_binned_prediction"][
                                        row
                                    ] = predicted_arrival
                            if (
                                (stop.name + " [arrival]") in nonempty.columns
                                and passage.id.value not in arrived_passages
                            ):
                                # discard journey data
                                arrival_time = nonempty[stop.name + " [arrival]"].iloc[
                                    -1
                                ]
                                arrived[row] = arrival_time
                                arrived_passages[passage.id.value] = arrival_time
                                # display prediction stats
                                prediction_results = evaluate_predictions(
                                    responses, passage, arrival_time
                                )
                                prediction_results["route"] = passage.route.map(
                                    lambda id: id.raw
                                ).optional()
                                prediction_results["target_stop"] = stop.id
                                if stats_output_file.exists():
                                    prediction_results.to_csv(
                                        str(stats_output_file),
                                        mode="a",
                                        header=False,
                                        index=False,
                                    )
                                else:
                                    prediction_results.to_csv(
                                        str(stats_output_file), index=False
                                    )
            response["average_time_prediction"] = my_predictions
            response["binned_average_time_prediction"] = binned_predictions
            response["arrived"] = arrived
            response["last_stop"] = last_stops
            display(response)
            responses.appendleft(response)
            # delete old arrival data
            for passage, arrival_time in list(arrived_passages.items()):
                if arrival_time < loop_start - timedelta(minutes=10):
                    del arrived_passages[passage]
            sleep(max(0, 10 - (datetime.now() - loop_start).total_seconds()))
        except KeyboardInterrupt:
            print("Exiting")
            return
        except Exception as e:
            # print(f"Got an exception: {e}")
            traceback.print_exc()
            print()
            print("Continuing…")
            sleep(max(0, 10 - (datetime.now() - loop_start).total_seconds()))


def evaluate_predictions(
    responses: Deque[DataFrame], passage: Passage, arrival_time: datetime
) -> DataFrame:
    print("=" * 100)
    passage_id = passage.id.map(lambda id: id.raw).optional()
    responses_with_passage = [
        r
        for r in responses
        if passage_id in r.index
        and r["average_time_prediction"].loc[passage_id] is not pd.NaT
    ]
    print(f"Bus {passage.vehicle} arrived – {len(responses_with_passage)} snapshots.")
    df = pd.DataFrame()
    df["poll_time"] = [r["poll_time"].loc[passage_id] for r in responses_with_passage]
    df["prediction"] = [
        r["average_time_prediction"].loc[passage_id] for r in responses_with_passage
    ]
    df["binned_prediction"] = [
        r["binned_average_time_prediction"].loc[passage_id]
        for r in responses_with_passage
    ]
    df["day_binned_prediction"] = [
        r["day_binned_prediction"].loc[passage_id] for r in responses_with_passage
    ]
    df["real-time"] = [
        r["predicted_arrival"].loc[passage_id] for r in responses_with_passage
    ]
    df["last_stop"] = [r["last_stop"].loc[passage_id] for r in responses_with_passage]
    df["sections"] = [r["sections"].loc[passage_id] for r in responses_with_passage]
    df["arrival_time"] = arrival_time
    df["error (s)"] = df["prediction"] - arrival_time
    df["error (s)"] = df["error (s)"].apply(lambda td: td.total_seconds())
    df["binned error (s)"] = df["binned_prediction"] - arrival_time
    df["binned error (s)"] = df["binned error (s)"].apply(lambda td: td.total_seconds())
    df["day-binned error (s)"] = (
        df["day_binned_prediction"] - arrival_time
    )  # error subtracting datetimes with different time zones
    df["day-binned error (s)"] = df["day-binned error (s)"].apply(
        lambda td: td.total_seconds()
    )
    df["real-time error (s)"] = df["real-time"] - arrival_time
    df["real-time error (s)"] = df["real-time error (s)"].apply(
        lambda td: td.total_seconds()
    )

    copy = df.copy()

    copy["prediction"] = copy["prediction"].apply(to_time)
    copy["arrival_time"] = copy["arrival_time"].apply(to_time)
    copy["binned_prediction"] = copy["binned_prediction"].apply(to_time)
    copy["day_binned_prediction"] = copy["day_binned_prediction"].apply(to_time)
    copy["real-time"] = copy["real-time"].apply(to_time)
    copy["poll_time"] = copy["poll_time"].apply(to_time)
    print(copy.to_string())
    print("=" * 100)
    return df


def train_average_predictors(journeys: DataFrame, target: str) -> Dict[str, Any]:
    target_index = journeys.columns.get_loc(target)
    print(f"Training {target_index} average predictors:")
    output = {}
    for last_index in range(target_index):
        print(f"- {last_index + 1} of {target_index}")
        last = journeys.columns[last_index]
        predictor = train_average_predictor(journeys, last, target)
        if predictor is not None:
            output[last] = predictor
    return output


def train_average_predictor(
    journeys: DataFrame, last: str, target: str
) -> Optional[Any]:
    journeys = journeys[pd.notnull(journeys[target]) & pd.notnull(journeys[last])]
    y = travel_times(journeys, [], last, target).astype("int64") / 1_000_000_000
    if len(y) > 0:
        predictor = DummyRegressor(strategy="median")
        predictor.fit(journeys, y)
        return predictor
    else:
        return None


def train_day_binned_predictors(
    journeys: DataFrame, target: str, bins: List[time]
) -> Callable[[str, datetime], Optional[Any]]:
    def train_predictors(
        journeys: DataFrame, last: str, target: str, bins: List[time]
    ) -> Dict[int, Dict[time, Any]]:
        predictors: Dict[int, Dict[time, Any]] = {}
        journey_days = journeys[last].apply(lambda dt: dt.weekday())
        for day in journey_days.unique():
            bin_journeys = journeys[journey_days == day]
            predictors[day] = train_binned_predictors(bin_journeys, last, target, bins)
        return predictors

    def train_binned_predictors(
        journeys: DataFrame, last: str, target: str, bins: List[time]
    ) -> Dict[time, Any]:
        ps = {}
        for start, end in pairwise(bins):
            journey_times = journeys[last].apply(to_time)
            if len(journey_times) != 0:
                bin_journeys = journeys[
                    (journey_times >= start) & (journey_times <= end)
                ]
                predictor = train_average_predictor(bin_journeys, last, target)
                if predictor is not None:
                    ps[start] = predictor
        return ps

    target_index = journeys.columns.get_loc(target)
    print(f"Training {target_index} day-binned-average predictors:")
    predictors: Dict[str, Dict[int, Dict[time, Any]]] = {}
    for last_index in range(target_index):
        print(f"- {last_index + 1} of {target_index}")
        last = journeys.columns[last_index]
        predictors[last] = train_predictors(journeys, last, target, bins)

    def select_predictor(target: str, observation_time: datetime) -> Optional[Any]:
        predictor = predictors.get(target)
        if predictor is None:
            return None
        else:
            inner = predictor.get(observation_time.weekday())
            if inner is None:
                return None
            else:
                times_before = [t for t in bins if t < observation_time.time()]
                inner_inner = inner.get(times_before[-1])
                return inner_inner

    return select_predictor


def train_binned_average_predictors(
    journeys: DataFrame, target: str, bins: List[time]
) -> Callable[[str, time], Optional[Any]]:
    def train_predictors(
        journeys: DataFrame, last: str, target: str, bins: List[time]
    ) -> Dict[time, Any]:
        ps = {}
        for start, end in pairwise(bins):
            journey_times = journeys[last].apply(to_time)
            if len(journey_times) != 0:
                bin_journeys = journeys[
                    (journey_times >= start) & (journey_times <= end)
                ]
                predictor = train_average_predictor(bin_journeys, last, target)
                if predictor is not None:
                    ps[start] = predictor
        return ps

    target_index = journeys.columns.get_loc(target)
    print(f"Training {target_index} binned-average predictors:")
    predictors: Dict[str, Dict[time, Any]] = {}
    for last_index in range(target_index):
        print(f"- {last_index + 1} of {target_index}")
        last = journeys.columns[last_index]
        predictors[last] = train_predictors(journeys, last, target, bins)

    def select_predictor(target: str, observation_time: time) -> Optional[Any]:
        times_before = [t for t in bins if t < observation_time]
        predictor = predictors.get(target)
        if predictor is None:
            return None
        else:
            return predictor.get(times_before[-1])

    return select_predictor


def to_time(dt: Union[datetime, Any]) -> Union[time, Any]:
    if dt is pd.NaT:
        return dt
    else:
        try:
            time = dt.time()
            return time.replace(second=round(time.second), microsecond=0)
        except AttributeError:
            return dt


def display(df: DataFrame) -> None:
    df["scheduled"] = df["scheduled_arrival"].apply(to_time)
    df["real-time"] = df["predicted_arrival"].apply(to_time)
    df["prediction"] = df["average_time_prediction"].apply(to_time)
    df["binned_prediction"] = df["binned_average_time_prediction"].apply(to_time)
    df["day_binned"] = df["day_binned_prediction"].apply(to_time)
    df["arrived_at"] = df["arrived"].apply(to_time)
    print(
        df[
            [
                "route",
                "vehicle",
                "scheduled",
                "real-time",
                "prediction",
                "binned_prediction",
                "day_binned",
                "sections",
                "arrived_at",
            ]
        ]
    )


def show_passage(passage: Passage) -> str:
    vehicle = passage.vehicle.map(lambda i: i.raw).or_else("None")
    position = passage.position.map(str).or_else("None")
    scheduled = (
        passage.time.arrival.bind(lambda t: t.scheduled)
        .map(lambda t: t.time().isoformat())
        .or_else("None")
    )
    predicted = (
        passage.time.arrival.bind(lambda t: t.actual_or_prediction)
        .map(lambda t: t.time().isoformat())
        .or_else("None")
    )
    return f"{vehicle:^19} - {scheduled:^8} - {predicted:^8}"


def containing_sections(
    sections: List[RouteSection], longitude: DegreeLongitude, latitude: DegreeLatitude
) -> Set[int]:
    return {
        i for i, section in enumerate(sections) if section.contains(longitude, latitude)
    }


if __name__ == "__main__":
    main()
