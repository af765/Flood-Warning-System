from floodsystem.geo import displayStationLocation, stationObjectsByRiver
from floodsystem.stationdata import build_station_list

rivers = ["River Cam", "River Thames"]
stations = build_station_list()
stations = stationObjectsByRiver(stations, rivers)

displayStationLocation(stations)

