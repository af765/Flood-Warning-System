from floodsystem.plot import plot_water_level_with_fit
from matplotlib.dates import date2num
from floodsystem.flood import stations_highest_rel_level
from floodsystem.stationdata import build_station_list, update_water_levels
from floodsystem.datafetcher import fetch_measure_levels
from datetime import timedelta

stations = build_station_list()
update_water_levels(stations)

highest_rel = stations_highest_rel_level(stations, 6)
dt = 2
p = 4
for station in highest_rel:
    dates, levels = fetch_measure_levels(station[0].measure_id, dt=timedelta(days=dt))
    plot_water_level_with_fit(station[0], dates, levels, p)