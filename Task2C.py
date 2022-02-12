from floodsystem.stationdata import build_station_list, update_water_levels
from floodsystem.flood import stations_highest_rel_level

def run():
    """Requirements for Task 2C"""

    # Build list of stations
    stations = build_station_list()
    update_water_levels(stations)

    stations_high = stations_highest_rel_level(stations, 10)
    for station in stations_high:
        print(station[0].name + ": " + str(station[1]))

run()
