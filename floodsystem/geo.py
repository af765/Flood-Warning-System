# Copyright (C) 2018 Garth N. Wells
#
# SPDX-License-Identifier: MIT
"""This module contains a collection of functions related to
geographical data.

"""

from .utils import sorted_by_key  # noqa
from haversine import haversine


def stations_by_distance(stations, p):
    """" Returns a list of tuples of the form (station, distance) of all the stations
    from the point p. Sorted by distance"""
    station_dist = []
    for station in stations:
        station_dist.append((station,haversine(station.coord,p)))
    station_dist = sorted_by_key(station_dist, 1)
    return station_dist

def stations_within_radius(stations, centre, r):
    """Returns a list of the names of stations that fall within a distance r from a
    point centre"""
    stations_within_r = []
    for station in stations:
        dist = haversine(station.coord, centre)
        if (dist < r):
            stations_within_r.append(station.name)
    stations_within_r.sort()

    return stations_within_r

def rivers_with_stations(stations):
    """Returns a list of rivers with a monitoring stations"""

    rivers = []
    for station in stations:
        if (station.river not in rivers):
            rivers.append(station.river)
    return rivers

def stations_by_river(stations):
    """Returns a dictionary mapping river names (the key) to a list of station opjects on a given river (in alphabetical order)"""
    river_dict = {}
    rivers = rivers_with_stations(stations) #Get list of rivers to search for
    for river in rivers: #iterate over rivers
        stationList = []
        for station in stations: #iterate over all stations
            if station.river == river: #if station is on the river add it
                stationList.append(station.name)
        river_dict[river]=sorted(stationList)
    
    return river_dict

#def rivers_by_station_number(stations, N):
    #riversList = stations_by_river(stations)
   # riverNumber = [()]
   # for river, stationList in riversList:
       # riverNumber.append(river, len(stationList))
    
  #  riverNumber.sort(key= lambda x:x[1])
   # extraStations = 0

   # for i in range(N, len(riverNumber)):
       # if riverNumber[i][1] == riverNumber[N-1][1]:
       #     extraStations += 1
      #  else:
       #     break
    
  #  N += extraStations
  #  return riverNumber[:N] #This may need to be N+1


