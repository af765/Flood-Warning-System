from floodsystem.flood import stations_level_over_threshold
from matplotlib.dates import date2num
from  floodsystem.analysis import polyfit
from floodsystem.datafetcher import fetch_measure_levels
from floodsystem.geo import displayStationLocation, stations_by_river, stations_within_radius
from floodsystem.plot import plot_water_level_with_fit, plot_water_levels
from floodsystem.station import inconsistent_typical_range_stations
from floodsystem.stationdata import build_station_list, update_water_levels
import numpy as np
import datetime

###Areas to improve:
    #Better method for computing a point on the polynomial fit. Very flat lines have sharp rises at the end, 'tricking' the algorithm into thinking there is an issue
    #Calibrate the below numbers, rather than taking 'guesses'


#Constants to adjust graphing results:
weightRelativeLevel = 10 #weight of the current water level
weightRisingWaterLevel = 1.5 #weight of rising water level
weightFallingWaterLevel = 0.9 #weight of lowering water level
stationWithinRadiusToCheck = [5,15,45,100] #distances from stations to check
stationWithinRadiusWeight = [0.05, 0.01, 0, 0] #weights of each distance above. Note that these are additive
stationOnRiverWeight = 0 #on the same river weight
cutoff = [150,100,60,30] #severe, high, moderate, low. Note these values are dependent on minimum level
orderOfInitialAssignment = 3 #the power that the current water level is taken to
orderofRisingLevel = 1.4 #the power that the rising water level is taken to
minimumLevel = 1.2 #minimum relative water level to consider rivers for further analysis
daysToConsider = 1 #how many days to consider for polynomial plot
output = ["Severe"] #"Severe", "High", "Moderate", "Low", "No Risk"

#Output Function defined for use later. In practice this would be moved to another file then imported in.
def OutputData(stations,statusDictionary, warningLevel, levelCutoff):
    """Function takes in a list of stations, the status dictionary and the desired warning levels, then plots the location of the most vulnerable stations and outputs a list of most vulnerable towns"""
    output = []
    for station in stations:
        if ("Severe" in warningLevel) and (statusDictionary[station.name] >= levelCutoff[0]):
                output.append((station, statusDictionary[station.name]))
        if "High" in warningLevel:
            if (statusDictionary[station.name] < levelCutoff[0]) and statusDictionary[station.name] >= levelCutoff[1]:
                output.append((station, statusDictionary[station.name]))
        if "Moderate" in warningLevel:
            if (statusDictionary[station.name] < levelCutoff[1]) and statusDictionary[station.name] >= levelCutoff[2]:
                output.append((station, statusDictionary[station.name]))
        if "low" in warningLevel:
            if (statusDictionary[station.name] < levelCutoff[2]) and statusDictionary[station.name] >= levelCutoff[3]:
                output.append((station, statusDictionary[station.name]))
        if "NoRisk" in warningLevel and statusDictionary[station.name] < levelCutoff[3]:
                output.append((station, statusDictionary[station.name]))

    outputStationList = []
    for element in output:
        outputStationList.append(element[0])

    print("STATUS: Attempting to plot level graphs of stations with {} level warning".format(warningLevel)) 
    for outputStation in outputStationList:
            dt = 2
            dates, levels = fetch_measure_levels(outputStation.measure_id, dt=datetime.timedelta(days=5))
            try:
                plot_water_levels(outputStation, dates, levels)
                #plot_water_level_with_fit(outputStation, dates, levels, 5)
            except:
                print("ERROR: Failed to plot station {}".format(outputStation.name))
            
    if outputStationList != None:
        displayStationLocation(outputStationList)
    else:
        print("STATUS: No Severe Level Status Rivers")
    mostVulnerableTowns = []
    for i in outputStationList:
        if i.town != None:
            mostVulnerableTowns.append(i.town)
        else:
            print("RESULT: Station {} has no reported town".format(i.name))

    print("RESULT: The Most Vulnerbale Towns are: {}".format(mostVulnerableTowns))
    return(mostVulnerableTowns)


#Create list of stations to analyse
stations = build_station_list()

#Remove any stations which could cause issues due to inconsistent imported data
inconsistentStations = inconsistent_typical_range_stations(stations)
for i, station in enumerate(stations):
    if station.name in inconsistentStations:
        stations.pop(i)

#update current water levels
update_water_levels(stations)

#create dictionary to store status of each station
statusDictionary = {}
for station in stations:
    statusDictionary[station.name] = 0

NewStationListTuple = stations_level_over_threshold(stations, minimumLevel)
newStations = []
currentLevels = []
for newStationTuple in NewStationListTuple:
    newStations.append(newStationTuple[0])

#Create initial risk only based on current water level. Parameters for this can be adjusted above
for newStation in newStations:
    statusDictionary[newStation.name] = weightRelativeLevel*(newStation.relative_water_level()**orderOfInitialAssignment)

dateLevels = [] #contains array of tuples (dates, levels)

print("STATUS: Fetching historical Data for required stations")
for newStation in newStations:
    dateLevels.append(fetch_measure_levels(newStation.measure_id, dt=datetime.timedelta(days=daysToConsider)))
    #print("station {} complete".format(newStation.name))


print("STATUS: Calculating polynomials and Derivatives")
#create polynomial fits for each station's data. This should still be ordered the same as the original stations array
polyArray = []
indicesToRemove = []
for i, dateLevel in enumerate(dateLevels):
    try:
        polyArray.append(polyfit(dateLevel[0], dateLevel[1], 5))
    except:
        print("ERROR: No historical data found for station {}. Removing this river from future consideration.".format(newStations[i].name))

        #Create URL to check the data
        # Current time (UTC)
        now = datetime.datetime.utcnow()
        dt=datetime.timedelta(days=10)
        # Start time for data
        start = now - dt

        # Construct URL for fetching data
        url_base = newStations[i].measure_id
        url_options = "/readings/?_sorted&since=" + start.isoformat() + 'Z'
        url = url_base + url_options
        print("Link to view data: {}".format(url))
        indicesToRemove.append(i)

        newStations.pop(i) #remove incompatable station

#remove required entries from the DateLevels array:
for index in sorted(indicesToRemove, reverse=True): #Go in reverse order to not screw with indices. 
    del dateLevels[index]


#Evaluate the value of the derivative (slope) at current time. This should give a warning as to how the water level is changing, and whether it is worrying
polyDerivative = []
for poly, offset in polyArray:
    polyDerivative.append(np.polyval(np.polyder(poly), date2num(datetime.datetime.utcnow())-offset))

#Edit the values of the warning depending on the water level. If the water level is high, when still rising, this is major cause for concern
#Use quadratic term for increasing water level and linear term for decreasing, to favour caution
print("STATUS: Adding warning level for rising/lowering rivers")
for newStation, polyDerivative in zip(newStations, polyDerivative):
    if polyDerivative>0:
        alpha = weightRisingWaterLevel*newStation.relative_water_level()**orderofRisingLevel
    else:
        alpha = weightFallingWaterLevel*newStation.relative_water_level()
    statusDictionary[newStation.name] += (alpha*polyDerivative)

#Add small warning to stations within a certain radius of at risk rivers, and on the same rivers

#Within radius warning. Additional warning proportional to the risk on the river which others are nearby
print("STATUS: Looking for nearby stations")
for newStation in newStations:
    nearbyStations = stations_within_radius(stations, newStation.coord, stationWithinRadiusToCheck[0])
    for nearbyStation in nearbyStations:
        statusDictionary[nearbyStation] += stationWithinRadiusWeight[0]*statusDictionary[newStation.name]
    nearbyStations = stations_within_radius(stations, newStation.coord, stationWithinRadiusToCheck[1])
    for nearbyStation in nearbyStations:
        statusDictionary[nearbyStation] += stationWithinRadiusWeight[1]*statusDictionary[newStation.name]
    nearbyStations = stations_within_radius(stations, newStation.coord, stationWithinRadiusToCheck[2])
    for nearbyStation in nearbyStations:
        statusDictionary[nearbyStation] += stationWithinRadiusWeight[2]*statusDictionary[newStation.name]
        nearbyStations = stations_within_radius(stations, newStation.coord, stationWithinRadiusToCheck[3])
    for nearbyStation in nearbyStations:
        statusDictionary[nearbyStation] += stationWithinRadiusWeight[3]*statusDictionary[newStation.name]

#On same river warning
print("STATUS: Looking for other stations on at risk rivers")
stationsOnRiver = stations_by_river(stations)

for newStation in newStations:
    river = newStation.river
    stationsOnNewStationRiver = stationsOnRiver[river]
    for station in stationsOnNewStationRiver:
        statusDictionary[station] +=  stationOnRiverWeight*statusDictionary[newStation.name] #Only small because in theory all stations on a river should have roughly the same risk already


#output a list of  rivers that are most at risk. 
OutputData(stations, statusDictionary, output, cutoff)