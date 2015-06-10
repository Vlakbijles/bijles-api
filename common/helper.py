import numpy as np


def latlon_distance(lat1, lon1, lat2, lon2):
    """
    Function for calculating the distance in meters between two locations.
    These location must be specified using the latitude and longitude in degrees.

    """
    # radius of the earth
    radius = 6371000
    # convert degrees to radians
    lat1 = (lat1 * np.pi) / 180
    lon1 = (lon1 * np.pi) / 180
    lat2 = (lat2 * np.pi) / 180
    lon2 = (lon2 * np.pi) / 180
    # calculate distance according to the Haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = np.power(np.sin(dlat / 2), 2) + np.cos(lat1) * np.cos(lat2) * np.power(np.sin(dlon / 2), 2)
    intermediateResult = 2 * np.arctan2(np.sqrt(a), np.sqrt(1-a))
    distance = radius * intermediateResult
    return distance


if __name__ == '__main__':
    # print latlon_distance(51.8406674630333, 5.8606943459950, 51.8383746106916, 5.8603704063373)
    for _ in range(100000):
        print latlon_distance(51.8405505, 5.8605194, 51.7929038, 5.8495331)
    # print latlon_distance(51, 5, 41, -75)
