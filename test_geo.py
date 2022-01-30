from floodsystem.station import MonitoringStation
from floodsystem.geo import stations_by_distance, stations_within_radius, rivers_with_stations, stations_by_river, rivers_by_station_number
from haversine import haversine

a = MonitoringStation(label="a", station_id = 1, measure_id=1, coord=(1,1), river="A", town = "townA", typical_range=(5,10))
b = MonitoringStation(label="b", station_id = 2, measure_id=2, coord=(4,4), river="A", town = "townB",typical_range=(10,5))
c = MonitoringStation(label="c", station_id = 3, measure_id=3, coord=(3,3), river="B", town = "townC", typical_range=None)
stations = [a,b,c]

def test_stations_by_distance():
    stat = stations_by_distance(stations, (0,0))
    assert stat[0][0] == a
    assert stat[1][0] == c
    assert stat[2][0] == b

def test_stations_within_radius():
    assert stations_within_radius(stations, (2,2), 200) == ["a", "c"]

def test_rivers_with_stations():
    rivers = rivers_with_stations(stations)
    assert type(rivers)==list #make sure its a list
    for i in range(len(rivers)):
        assert type(rivers[i])==str
    assert "A" in rivers
    assert "B" in rivers

def test_stations_by_river():
    stationsByRiver = stations_by_river(stations)
    assert type(stationsByRiver)==dict #make sure its a dictionary
    keys = list(stationsByRiver.keys())
    values = stationsByRiver.values()
    assert type(keys[0])==str #make sure the keys are a string
    for key in keys:
        assert type(stationsByRiver[key])==list #make sure the stations for each river are in a list
    
    assert "a","b" in stationsByRiver["A"]
    assert "c" in stationsByRiver["B"]
    assert "c" not in stationsByRiver["A"]

def test_rivers_by_station_number():
    N=2
    riverByStationNumber = rivers_by_station_number(stations, N)

    assert len(riverByStationNumber)>=N
    for i in range(1,len(riverByStationNumber)):
        assert riverByStationNumber[i][1]<=riverByStationNumber[i-1][1]
    assert ('A',2) in riverByStationNumber

if __name__=="__main__":
    test_stations_by_distance()
    test_stations_within_radius()
    test_rivers_with_stations()
    test_stations_by_river()

