# Copyright (C) 2018 Garth N. Wells
#
# SPDX-License-Identifier: MIT
"""This module contains a collection of functions related to
geographical data.

"""

from .utils import sorted_by_key  # noqa
from haversine import haversine


def stations_by_distance(stations, p):
    station_dist = []
    for station in stations:
        station_dist.append((station,haversine(station.coord,p)))
    station_dist = sorted_by_key(station_dist, 1)

    return station_dist

def stations_within_radius(stations, centre, r):
    stations_within_r = []
    for station in stations:
        dist = haversine(station.coord, centre)
        if (dist < r):
            stations_within_r.append(station.name)
    stations_within_r.sort()

    return stations_within_r
