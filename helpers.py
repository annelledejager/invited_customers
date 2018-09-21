import math

MEAN_EARTH_RADIUS = 6371
DEGREES_TO_RADIANS = math.pi / 180.0


def get_shortest_distance_between_two_coordinates(lat1=0, lng1=0, lat2=0, lng2=0):
    try:
        # phi = 90 - latitude
        phi1 = (90.0 - lat1) * DEGREES_TO_RADIANS
        phi2 = (90.0 - lat2) * DEGREES_TO_RADIANS

        # theta = longitude
        theta1 = lng1 * DEGREES_TO_RADIANS
        theta2 = lng2 * DEGREES_TO_RADIANS
    except Exception as e:
        raise Exception(e)

    cos = (math.sin(phi1) * math.sin(phi2) * math.cos(theta1 - theta2) + math.cos(phi1) * math.cos(phi2))

    return math.acos(cos) * MEAN_EARTH_RADIUS


def convert_to_float(input):
    try:
        return float(input)
    except ValueError as e:
        raise Exception(e)
