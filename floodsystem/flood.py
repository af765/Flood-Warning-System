from .utils import sorted_by_key

def stations_level_over_threshold(stations, tol):
    """Returns a list of all the stations with a relative water level above a tolerance value """
    stations_over_tol = []
    for station in stations:
        if (station.relative_water_level() != None)and (station.relative_water_level() < 200):
            if station.relative_water_level()>tol:
                stations_over_tol.append((station, station.relative_water_level()))
        else:
            if station.relative_water_level() == None:
                reason = "No input data"
                #print("WARNING: Station \"{}\" removed from consideration due to invalid input data ({})".format(station.name, reason))
            else:
                reason = "Error due to extreme relative water level (>200)"
                print("WARNING: Station \"{}\" removed from consideration due to invalid input data ({})".format(station.name, reason))

    stations_over_tol = sorted_by_key(stations_over_tol, 1)
    stations_over_tol.reverse()
    return stations_over_tol

def stations_highest_rel_level(stations, N):
    """Returns the stations with the N highest relative water levels"""
    stations_high = []
    for station in stations:
        if ((station.relative_water_level() != None) and (station.relative_water_level() < 200) ): #Add filter to remove stations with clearly incorrect data
            stations_high.append((station, station.relative_water_level()))
        else:
            if station.relative_water_level() == None:
                reason = "No input data"
                #print("WARNING: Station \"{}\" removed from consideration due to invalid input data ({})".format(station.name, reason))
            else:
                reason = "Error due to extreme relative water level (>200)"
                print("WARNING: Station \"{}\" removed from consideration due to invalid input data ({})".format(station.name, reason))
    
    stations_high = sorted_by_key(stations_high, 1)
    stations_high.reverse()
    return stations_high[:N]
