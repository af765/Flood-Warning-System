from floodsystem.geo import rivers_with_stations, stations_by_river
from floodsystem.stationdata import build_station_list

stations = build_station_list()
rivers = rivers_with_stations(stations)
rivers.sort()
print("{} stations. First 10- {}".format(len(rivers), rivers[:10]))

stationsOnRivers = stations_by_river(stations)
print("River Aire: {} \n".format(stationsOnRivers["River Aire"]))
print("River Cam: {} \n".format(stationsOnRivers["River Cam"]))
print("River Thames: {} \n".format(stationsOnRivers["River Thames"]))

#I think this should work but don't have haversine installed to be able to check. Compliation crashes on reading haversine
