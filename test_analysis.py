from floodsystem.datafetcher import fetch_measure_levels
import datetime
from floodsystem.analysis import polyfit
from floodsystem.stationdata import build_station_list, update_water_levels
import numpy as np
#As require historic data cannot create test data set. Therefore assert the function works by ensuring the output is not None. 

def test_polyfit():
     # Build list of stations
    stations = build_station_list()

    # Find station 'Cam'
    for station in stations:
        if station.name == 'Girton':
            station_cam = station
            break

    # Fetch data over past 2 days
    dt = 2
    dates2, levels2 = fetch_measure_levels(
        station_cam.measure_id, dt=datetime.timedelta(days=dt))

    poly = polyfit(dates2, levels2, 4)
    assert poly != None
    assert type(poly) == tuple
    assert type(poly[0]) == np.poly1d #ensure the elements of the tuple are correct type
    assert type(poly[1]) == np.float64
