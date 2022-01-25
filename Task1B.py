from floodsystem.stationdata import build_station_list
from floodsystem.geo import stations_by_distance

stations = stations_by_distance(build_station_list(), (52.2053, 0.1218))

def print_data(station):
    """Cleans up the print statement by having it in one place so its easier to edit"""
    print(station[0].name, station[0].town, station[1], sep=", ")

print("The Closest 10 Rivers Are:", end="\n\n")
for station in stations[:10]:
    print_data(station)

print("\n\nThe Furthest 10 Rivers Are:", end="\n\n")
for station in stations[-10:]:
    print_data(station)
