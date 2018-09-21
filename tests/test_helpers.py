import unittest

from invited_customers.helpers import get_shortest_distance_between_two_coordinates, convert_to_float


class GetShortestDistanceBetweenTwoCoordinatesTestCase(unittest.TestCase):
    def setUp(self):
        super(GetShortestDistanceBetweenTwoCoordinatesTestCase, self).setUp()

    def test_valid_inputs(self):
        # When
        result = get_shortest_distance_between_two_coordinates(
            lat1=52.986375,
            lng1=-6.043701,
            lat2=53.339428,
            lng2=-6.257664)

        self.assertEqual(41.76872550078046, result)

    def test_invalid_inputs(self):
        # When
        with self.assertRaises(Exception) as ex:
            get_shortest_distance_between_two_coordinates(lng1='')

    def test_no_inputs(self):
        # When
        result = get_shortest_distance_between_two_coordinates()

        self.assertEqual(0, result)


class ConvertToFloatTestCase(unittest.TestCase):
    def setUp(self):
        super(ConvertToFloatTestCase, self).setUp()

    def test_success(self):
        # When
        result = convert_to_float(10)

        # Then
        self.assertEqual(type(result), float)

    def test_failure(self):
        # When
        with self.assertRaises(Exception):
            convert_to_float(None)
