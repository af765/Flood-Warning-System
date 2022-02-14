import matplotlib.pyplot as plt
from matplotlib.dates import date2num
from numpy import linspace
from datetime import datetime, timedelta
from .analysis import polyfit
from .datafetcher import fetch_measure_levels
from .stationdata import build_station_list

def plot_water_levels(station, dates, levels):
    """Plot the water level for a station for the past n days along with the typical
    high and low water levels"""
    # Plot
    plt.plot(dates, levels)
    plt.plot(dates ,[station.typical_range[0] for n in dates])
    plt.plot(dates ,[station.typical_range[1] for n in dates])

    # Add axis labels, rotate date labels and add plot title
    plt.xlabel('Date')
    plt.ylabel('Water Level (m)')
    plt.xticks(rotation=45);
    plt.title(station.name)

    # Display plot
    plt.tight_layout()  # This makes sure plot does not cut off date labels

    plt.show()

if __name__ == "__main__":
    stations = build_station_list()
    station = stations[5]

    dt = 10
    dates, levels = fetch_measure_levels(station.measure_id, dt=timedelta(days=dt))
    plot_water_levels(station, dates,levels)

def plot_water_level_with_fit(station, dates, levels, p):
    """Plots the historic water data (given by dates, levels) and the least-squares polynomial approximation (of order p)"""
    #create polynomial object and plot it using 30 data points spaced along the requested period (denoted by dates)
    #print(dates)
    poly, offset = polyfit(dates, levels, p)
    dateFloat = date2num(dates)
    plt.plot(dateFloat, poly(dateFloat-offset))

    #Plot exact data 
    plt.plot(dates,levels)

    #Format graph
    plt.xlabel('Date')
    plt.ylabel('Water Level (m)')
    plt.xticks(rotation=45)
    plt.title(station.name)
    plt.tight_layout()

    plt.show()


