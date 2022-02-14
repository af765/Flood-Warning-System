from matplotlib.dates import date2num
import numpy as np

def polyfit(dates, levels, p):
    """Returns a tuple of type (numpy.poly1D, float), where the first element is a least-squares polynomial fit of the dates, levels
    data and the float is a shift of the time axis due to the use of matplotlib.dates.date2num"""
    dateFloats = date2num(dates)
    #print(dateFloats)
    offset = dateFloats[0]
    dateFloats = dateFloats - offset
    p_coeff = np.polyfit(dateFloats, levels, p)
    poly = np.poly1d(p_coeff)
    returnObject = (poly, offset)
    return returnObject




