from .utils import sorted_by_key

def stations_level_over_threshold(stations, tol):
    stations_over_tol = []
    for station in stations:
        if (station.relative_water_level() != None):
            if station.relative_water_level()>tol:
                stations_over_tol.append((station, station.relative_water_level()))

    stations_over_tol = sorted_by_key(stations_over_tol, 1)
    stations_over_tol.reverse()
    return stations_over_tol
