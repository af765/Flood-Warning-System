from floodsystem.flood import stations_level_over_threshold
from matplotlib.dates import date2num
from  floodsystem.analysis import polyfit
from floodsystem.datafetcher import fetch_measure_levels
from floodsystem.geo import displayStationLocation, stations_by_river, stations_within_radius
from floodsystem.plot import plot_water_levels
from floodsystem.station import inconsistent_typical_range_stations
from floodsystem.stationdata import build_station_list, update_water_levels
import numpy as np
import datetime

#Constants to adjust graphing results:
weightRelativeLevel = 5
weightRisingWaterLevel = 0.5
weightFallingWaterLevel = 0.3
stationWithinRadiusToCheck = [5,15,45,100]
stationWithinRadiusWeight = [0.15, 0.1, 0.05, 0.025]
stationOnRiverWeight = 0
SevereCutOff = 60
HighCutOff = 40
ModerateCutOff = 25
LowCutOff = 10
orderOfInitialAssignment = 3
orderofRisingLevel = 1.4
minimumLevel = 1.2
daysToConsider = 1



#Create list of stations to analyse
stations = build_station_list()

#Remove any stations which could cause issues due to inconsistent imported data
inconsistentStations = inconsistent_typical_range_stations(stations)
for station in stations:
    if station.name in inconsistentStations:
        stations.pop()

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
for newStation in newStations:
    dateLevels.append(fetch_measure_levels(newStation.measure_id, dt=datetime.timedelta(days=daysToConsider)))
    print("station {} complete".format(newStation.name))


print("STATUS: Moving onto polynomials and Derivatives")
#create polynomial fits for each station's data. This should still be ordered the same as the original stations array
polyArray = []
for dateLevel in dateLevels:
    polyArray.append(polyfit(dateLevel[0], dateLevel[1], 5))

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
Severe = []
High =[]
Moderate = []
Low = []
NoRisk = []
for station in stations:
    if statusDictionary[station.name] >= SevereCutOff:
        Severe.append((station, statusDictionary[station.name]))
    elif statusDictionary[station.name] >= HighCutOff:
        High.append((station, statusDictionary[station.name]))
    elif statusDictionary[station.name] >= ModerateCutOff:
        Moderate.append((station, statusDictionary[station.name]))
    elif statusDictionary[station.name] >= LowCutOff:
        Low.append((station, statusDictionary[station.name]))
    else:
        NoRisk.append((station, statusDictionary[station.name]))

SevereStationList = []
for element in Severe:
    SevereStationList.append(element[0])
#print(SevereStationList)

print("STATUS: Attempting to plot level graphs of most vulnerable stations") 
for severeStation in SevereStationList:
        dt = 2
        dates, levels = fetch_measure_levels(severeStation.measure_id, dt=datetime.timedelta(days=5))
        plot_water_levels(severeStation, dates, levels)
if SevereStationList != None:
    displayStationLocation(SevereStationList)
else:
    print("STATUS: No Severe Level Status Rivers")