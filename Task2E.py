from floodsystem.plot import plot_water_levels
from floodsystem.flood import stations_highest_rel_level
from floodsystem.station import MonitoringStation
from floodsystem.stationdata import build_station_list, update_water_levels
from floodsystem.datafetcher import fetch_measure_levels
from datetime import datetime, timedelta

def run():
    stations = build_station_list()
    update_water_levels(stations)

    highest_rel = stations_highest_rel_level(stations, 5)
    print(highest_rel)
    for station in highest_rel:
        dt = 10
        dates, levels = fetch_measure_levels(station[0].measure_id, dt=timedelta(days=dt))
        plot_water_levels(station[0], dates, levels)

run()
