from floodsystem.station import MonitoringStation
from floodsystem.geo import stations_by_distance, stations_within_radius
from haversine import haversine

a = MonitoringStation(label="a", station_id = 1, measure_id=1, coord=(1,1), river=1, town = 1, typical_range=(5,10))
b = MonitoringStation(label="b", station_id = 1, measure_id=1, coord=(4,4), river=1, town = 1,typical_range=(10,5))
c = MonitoringStation(label="c", station_id = 1, measure_id=1, coord=(3,3), river=1, town = 1, typical_range=None)
stations = [a,b,c]

def test_stations_by_distance():
    stat = stations_by_distance(stations, (0,0))
    assert stat[0][0] == a
    assert stat[1][0] == c
    assert stat[2][0] == b

def test_stations_within_radius():
    assert stations_within_radius(stations, (2,2), 200) == ["a", "c"]

if __name__=="__main__":
    test_stations_by_distance()
    test_stations_within_radius()
