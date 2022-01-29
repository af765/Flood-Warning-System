from distutils.command import build
from floodsystem.geo import rivers_by_station_number
from floodsystem.stationdata import build_station_list

stations = build_station_list()

N=9
listOfRivers = rivers_by_station_number(stations, N)
print(listOfRivers)
