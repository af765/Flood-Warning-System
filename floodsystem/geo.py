# Copyright (C) 2018 Garth N. Wells
#
# SPDX-License-Identifier: MIT
"""This module contains a collection of functions related to
geographical data.

"""

from os import access
from .utils import sorted_by_key  # noqa
from haversine import haversine
import plotly.graph_objects as go
from numpy import average


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

def rivers_by_station_number(stations, N):
    """Returns a list of N tuples on the form (river name, number of stations on the river). These tuples are sorted in decreasing order of station numbers. 
    If many stations have the same number of stations as the 'Nth' river, these are also included."""
    
    riversList = stations_by_river(stations) #Get list of rivers to consider
    riverNumber = []
    for River in riversList:
        riverNumber.append((River, len(riversList[River]))) #Get tuple of (river name, number of stations)

    riverNumber.sort(key= lambda x:x[1], reverse=True) #Sort into decreasing numerical order
    
    #This code is used to include any rivers with equal number of stations to the 'final' one being output.
    extraStations = 0

#search through next few rivers to see how many have the same number of stations
    for i in range(N, len(riverNumber)):
        if riverNumber[i][1] == riverNumber[N-1][1]:
            extraStations += 1
        else:
            break #as items pre-sorted once the number is not equal can exit
    
    N += extraStations #adjust value of N
    return riverNumber[:N] #Return sliced array.


def displayStationLocation(stations, type = "basic"):
    """Displays a map showing the location of stations inputted. The inputs are:
        stations: A list of MonitoringStation objects to plot
        type: The type of map to plot. See https://plotly.com/python/mapbox-layers/#base-maps-in-layoutmapboxstyle for more details"""
    accessToken = "pk.eyJ1IjoidGpnNDkiLCJhIjoiY2t6MXFkZjk0MWlkNDJ2cXZoZ2VrbHUxZCJ9.q0CEoPcRyNTMzNS3_RyZFA"
    lattitude = []
    longitude = []
    name = []
    for station in stations:
        if station.coord[0] != None and station.coord[1] != None:
            lattitude.append(station.coord[0])
            longitude.append(station.coord[1])
            name.append("Station Name: {}\n River: {}".format(station.name, station.river))
    initialLongitude = average(longitude)
    initialLattitude = average(lattitude)
    fig = go.Figure(go.Scattermapbox(lat=lattitude, lon=longitude, mode = 'markers', marker = go.scattermapbox.Marker(size = 9), text=name))
    fig.update_layout(mapbox_style = type,autosize=True, hovermode='closest', mapbox=dict(accesstoken=accessToken,bearing=0, center=dict(lat=initialLattitude,lon=initialLongitude),pitch=0,zoom=7))
    fig.show()

def stationObjectsByRiver(stations, rivers):
    """Returns a list of Monitoring Station objects which are on the rivers input"""
    stationObjectsByRiverOutput = []
    for river in rivers:
        for station in stations:
            if station.river==river:
                stationObjectsByRiverOutput.append(station)
    return stationObjectsByRiverOutput
