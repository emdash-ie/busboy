"""
Utility functions for jupyter notebooks.
"""
import time
from collections import deque
from typing import Deque, List, Tuple

import ipyleaflet as lf

from busboy.database import DatabaseEntry
from busboy.map.map import Map


def plot_entries(
    m: Map,
    entries: List[DatabaseEntry],
    interval: float = 0.1,
    initial_delay: float = 0.5,
) -> None:
    """Displays a list of entries gradually on a leaflet map."""
    time.sleep(initial_delay)
    m.clear_layers()
    last = None
    for entry in sorted(entries, key=lambda e: e.poll_time):
        m._add_marker(
            entry.latitude, entry.longitude, entry.poll_time.time().isoformat()
        )
        if last is None or entry.poll_time != last:
            time.sleep(interval)
        last = entry.poll_time


def plot_entry_trail(
    m: Map,
    entries: List[DatabaseEntry],
    trail_size: int = 10,
    interval: float = 0.1,
    initial_delay: float = 1,
) -> None:
    time.sleep(initial_delay)
    m.clear_layers()
    trail: Deque[Tuple[DatabaseEntry, lf.Marker]] = deque()
    for entry in sorted(entries, key=lambda e: e.poll_time):
        if len(trail) == 0 or trail[-1][0].poll_time != entry.poll_time:
            time.sleep(interval)
        trail.append(
            (
                entry,
                m._add_marker(
                    entry.latitude, entry.longitude, entry.poll_time.time().isoformat()
                ),
            )
        )
        while len(trail) > trail_size:
            old_entry, layer = trail.popleft()
            m.remove_layer(layer)
