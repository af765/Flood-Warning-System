from floodsystem.station import MonitoringStation
from floodsystem.flood import stations_level_over_threshold, stations_highest_rel_level
from floodsystem.stationdata import build_station_list, update_water_levels

a = MonitoringStation(label="a", latest_level = 7, station_id = 1, measure_id=1, coord=(1,1), river="A", town = "townA", typical_range=(0.5,10))
b = MonitoringStation(label="b", latest_level = 7, station_id = 2, measure_id=2, coord=(4,4), river="A", town = "townB",typical_range=(0.2,10))
c = MonitoringStation(label="c", latest_level = 7, station_id = 3, measure_id=3, coord=(3,3), river="B", town = "townC", typical_range=(0,5))
stations = [a,b,c]

def test_stations_level_over_threshold():
    stations_by_tol = stations_level_over_threshold(stations, 0.7)
    assert stations_by_tol[0][0] == c

def test_stations_highest_rel_level():
    stations_high = stations_highest_rel_level(stations, 2)
    assert stations_high[0][0].name == "c"
    assert stations_high[1][0].name == "b"

if __name__ == "__main__":
    test_stations_level_over_threshold()
    test_stations_highest_rel_level()
