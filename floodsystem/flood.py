from .utils import sorted_by_key

def stations_level_over_threshold(stations, tol):
    """Returns a list of all the stations with a relative water level above a tolerance value """
    stations_over_tol = []
    for station in stations:
        if (station.relative_water_level() != None):
            if station.relative_water_level()>tol:
                stations_over_tol.append((station, station.relative_water_level()))

    stations_over_tol = sorted_by_key(stations_over_tol, 1)
    stations_over_tol.reverse()
    return stations_over_tol

def stations_highest_rel_level(stations, N):
    """Returns the stations with the N highest relative water levels"""
    stations_high = []
    for station in stations:
        if (station.relative_water_level() != None):
            stations_high.append((station, station.relative_water_level()))

    stations_high = sorted_by_key(stations_high, 1)
    stations_high.reverse()
    return stations_high[:N]
