import unittest

from StringIO import StringIO
from invited_customers.invited_customers import InvitedCustomers
from mock import patch, ANY, mock_open


class InvitedCustomersBaseCase(unittest.TestCase):
    def setUp(self):
        super(InvitedCustomersBaseCase, self).setUp()
        self.customer = {"latitude": "52.986375", "user_id": 12, "name": "Christina McArdle", "longitude": "-6.043701"}


class InvitedCustomersTestCase(InvitedCustomersBaseCase):
    def setUp(self):
        super(InvitedCustomersTestCase, self).setUp()

    @patch('invited_customers.invited_customers.json.loads')
    @patch('invited_customers.invited_customers.open')
    @patch('invited_customers.invited_customers.customers_log')
    def test_success(self, mock_log, mock_open, mock_json_loads):
        # Given
        mock_open.return_value = '1'
        mock_json_loads.return_value = self.customer
        expected_result = '12 Christina McArdle\n'

        # When
        with patch('sys.stdout', new=StringIO()) as fake_output:
            InvitedCustomers().get()

        # Then
        self.assertEqual(fake_output.getvalue(), expected_result)

    @patch('invited_customers.invited_customers.json.loads')
    @patch('invited_customers.invited_customers.open')
    @patch('invited_customers.invited_customers.customers_log')
    def test_diff_radius_success(self, mock_log, mock_open, mock_json_loads):
        # Given
        mock_open.return_value = '1'
        mock_json_loads.return_value = self.customer
        expected_result = ''

        # When
        with patch('sys.stdout', new=StringIO()) as fake_output:
            InvitedCustomers(radius=20).get()

        # Then
        self.assertEqual(fake_output.getvalue(), expected_result)


class GetTestCase(InvitedCustomersBaseCase):
    def setUp(self):
        super(GetTestCase, self).setUp()

    @patch('invited_customers.invited_customers.InvitedCustomers._print_invited_customers')
    @patch('invited_customers.invited_customers.sorted')
    @patch('invited_customers.invited_customers.InvitedCustomers._get_invited_customers')
    @patch('invited_customers.invited_customers.customers_log')
    def test_success(self, mock_log, mock_get_invited_customers, mock_sorted, mock_print_invited_customers):
        # When
        InvitedCustomers().get()

        # Then
        mock_sorted.assert_called_once_with(mock_get_invited_customers.return_value, key=ANY)
        mock_print_invited_customers.assert_called_once_with(mock_sorted.return_value)

    @patch('invited_customers.invited_customers.InvitedCustomers._print_invited_customers')
    @patch('invited_customers.invited_customers.sorted')
    @patch('invited_customers.invited_customers.InvitedCustomers._get_invited_customers')
    @patch('invited_customers.invited_customers.customers_log')
    def test_success_logging(self, mock_log, mock_get_invited_customers, mock_sorted, mock_print_invited_customers):
        # Given
        result = [{'distance': 10.566936288936617, 'user_id': 4, 'name': u'Ian Kehoe'}]
        mock_sorted.return_value = result

        # When
        InvitedCustomers().get()

        # Then
        call_args = mock_log.info.call_args[0][0]
        self.assertEqual(call_args, "Result: {}".format(result))


class FormatCustomerTestCase(InvitedCustomersBaseCase):
    def setUp(self):
        super(FormatCustomerTestCase, self).setUp()

    def test_success(self):
        # Given
        distance = 120

        # When
        result = InvitedCustomers()._format_customer(self.customer, distance)

        # Then
        self.assertEqual(result, {'distance': 120, 'user_id': 12, 'name': 'Christina McArdle'})

    @patch('invited_customers.invited_customers.customers_log')
    def test_failure(self, mock_log):
        # Given
        customer = {}
        distance = 120

        # When
        with self.assertRaises(Exception):
            InvitedCustomers()._format_customer(customer, distance)

        # Then
        mock_log.error.assert_called_once_with('Invalid customer format')


class GetDistanceFromOfficeTestCase(InvitedCustomersBaseCase):
    def setUp(self):
        super(GetDistanceFromOfficeTestCase, self).setUp()

    @patch('invited_customers.invited_customers.get_shortest_distance_between_two_coordinates')
    def test_success(self, mock_helper):
        # When
        InvitedCustomers()._get_distance_from_office(1, 2)

        # Then
        mock_helper.assert_called_once_with(1, 2, 53.339428, -6.257664)

    @patch('invited_customers.invited_customers.get_shortest_distance_between_two_coordinates')
    def test_return_value_success(self, mock_helper):
        # When
        result = InvitedCustomers()._get_distance_from_office(1, 2)

        # Then
        self.assertEqual(result, mock_helper.return_value)


class ParseCustomerTestCase(InvitedCustomersBaseCase):
    def setUp(self):
        super(ParseCustomerTestCase, self).setUp()

    def test_success(self):
        # When
        InvitedCustomers()._parse_customer(self.customer)

    @patch('invited_customers.invited_customers.customers_log')
    def test_failure(self, mock_log):
        # Given
        customer = []

        # When
        with self.assertRaises(Exception):
            InvitedCustomers()._parse_customer(customer)

        # Then
        mock_log.error.assert_called_once_with('Schema validation failed')


class GetInvitedCustomerTestCase(InvitedCustomersBaseCase):
    def setUp(self):
        super(GetInvitedCustomerTestCase, self).setUp()

    @patch('invited_customers.invited_customers.customers_log')
    @patch('invited_customers.invited_customers.InvitedCustomers._get_distance_from_office')
    @patch('invited_customers.invited_customers.convert_to_float')
    @patch('invited_customers.invited_customers.InvitedCustomers._parse_customer')
    @patch('invited_customers.invited_customers.json.loads')
    def test_success(self, mock_json_loads, mock_parser_customer, mock_to_float, mock_get_distance_from_office,
                     mock_log):
        # Given
        mock_to_float.side_effect = [1.0, 2.0]
        mock_json_loads.return_value = self.customer
        mock_get_distance_from_office.return_value = 10

        # When_
        with patch("__builtin__.open", mock_open(read_data='')) as mock_file:
            mock_file.return_value = [0]
            InvitedCustomers()._get_invited_customers()

        # Then
        mock_json_loads.assert_called_once_with(0)
        mock_parser_customer.assert_called_once_with(mock_json_loads.return_value)
        self.assertEqual(2, mock_to_float.call_count)
        mock_get_distance_from_office.assert_called_once_with(1.0, 2.0)
        mock_log.debug.assert_called_once_with('User Id: 12, Distance: 10 km')

    @patch('invited_customers.invited_customers.customers_log')
    @patch('invited_customers.invited_customers.InvitedCustomers._get_distance_from_office')
    @patch('invited_customers.invited_customers.convert_to_float')
    @patch('invited_customers.invited_customers.InvitedCustomers._parse_customer')
    @patch('invited_customers.invited_customers.json.loads')
    def test_success_customers(self, mock_json_loads, mock_parser_customer, mock_to_float,
                               mock_get_distance_from_office, mock_log):
        # Given
        mock_to_float.side_effect = [1.0, 2.0]
        mock_get_distance_from_office.return_value = 80
        mock_json_loads.return_value = {"latitude": "52.986375", "user_id": 12, "name": "Christina McArdle",
                                        "longitude": "-6.043701"}
        expected_result = [{
            'distance': 80,
            'user_id': 12,
            'name': 'Christina McArdle'
        }]

        # When_
        with patch("__builtin__.open", mock_open(read_data='')) as mock_file:
            mock_file.return_value = '1'
            result = InvitedCustomers()._get_invited_customers()

        # Then
        self.assertEqual(result, expected_result)

    @patch('invited_customers.invited_customers.customers_log')
    @patch('invited_customers.invited_customers.InvitedCustomers._get_distance_from_office')
    @patch('invited_customers.invited_customers.convert_to_float')
    @patch('invited_customers.invited_customers.InvitedCustomers._parse_customer')
    @patch('invited_customers.invited_customers.json.loads')
    def test_success_no_customers_in_file(self, mock_json_loads, mock_parser_customer, mock_to_float,
                                          mock_get_distance_from_office, mock_log):
        # Given
        mock_to_float.side_effect = [1.0, 2.0]

        # When_
        with patch("__builtin__.open", mock_open(read_data='')):
            result = InvitedCustomers()._get_invited_customers()

        # Then
        self.assertEqual(result, [])

    @patch('invited_customers.invited_customers.customers_log')
    @patch('invited_customers.invited_customers.InvitedCustomers._get_distance_from_office')
    @patch('invited_customers.invited_customers.convert_to_float')
    @patch('invited_customers.invited_customers.InvitedCustomers._parse_customer')
    @patch('invited_customers.invited_customers.json.loads')
    def test_success_no_customers_within_radius(self, mock_json_loads, mock_parser_customer, mock_to_float,
                                                mock_get_distance_from_office, mock_log):
        # Given
        mock_to_float.side_effect = [1.0, 2.0]
        mock_get_distance_from_office.return_value = 120

        # When_
        with patch("__builtin__.open", mock_open(read_data='')) as mock_file:
            mock_file.return_value = '1'
            result = InvitedCustomers()._get_invited_customers()

        # Then
        self.assertEqual(result, [])


class PrintInvitedCustomerTestCase(InvitedCustomersBaseCase):
    def setUp(self):
        super(PrintInvitedCustomerTestCase, self).setUp()

    def test_success(self):
        # Given
        customers = [
            {'distance': 10.566936288936617, 'user_id': 4, 'name': u'Ian Kehoe'},
            {'distance': 23.28732066320704, 'user_id': 5, 'name': u'Nora Dempsey'},
            {'distance': 24.085360019065416, 'user_id': 6, 'name': u'Theresa Enright'},
            {'distance': 83.53253116787984, 'user_id': 8, 'name': u'Eoin Ahearn'},
        ]
        expected_output = '4 Ian Kehoe\n5 Nora Dempsey\n6 Theresa Enright\n8 Eoin Ahearn\n'
        # When
        with patch('sys.stdout', new=StringIO()) as fake_output:
            InvitedCustomers()._print_invited_customers(customers)

        # Then
        self.assertEqual(fake_output.getvalue(), expected_output)
