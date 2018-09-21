import json

from jsonschema import validate

from json_schema import CUSTOMER_SCHEMA
from helpers import get_shortest_distance_between_two_coordinates, convert_to_float
from logger import customers_log


DEFAULT_RADIUS = 100

OFFICE_LATITUDE = 53.339428
OFFICE_LONGITUDE = -6.257664


class InvitedCustomers(object):
    def __init__(self, radius=DEFAULT_RADIUS):
        self.radius = radius

    @staticmethod
    def _format_customer(customer, distance):
        try:
            return {
                'name': customer['name'],
                'user_id': customer['user_id'],
                'distance': distance
            }
        except KeyError as e:
            customers_log.error('Invalid customer format')
            raise Exception(e)

    @staticmethod
    def _get_distance_from_office(lat, lng):
        return get_shortest_distance_between_two_coordinates(lat,
                                                             lng,
                                                             OFFICE_LATITUDE,
                                                             OFFICE_LONGITUDE)

    @staticmethod
    def _parse_customer(customer):
        try:
            validate(customer, CUSTOMER_SCHEMA)
        except Exception as e:
            customers_log.error('Schema validation failed')
            raise Exception(e)

    def _get_invited_customers(self):
        invited_customers = []
        for line in open('invited_customers/customers.txt', 'r'):
            customer = json.loads(line)
            self._parse_customer(customer)

            lat = convert_to_float(customer['latitude'])
            lng = convert_to_float(customer['longitude'])
            distance = self._get_distance_from_office(lat, lng)

            customers_log.debug('User Id: {}, Distance: {} km'.format(customer['user_id'], distance))

            if distance < self.radius:
                invited_customers.append(self._format_customer(customer, distance))

        return invited_customers

    def _print_invited_customers(self, customers):
        for customer in customers:
            print '{} {}'.format(customer['user_id'], customer['name'])

    def get(self):
        customers_log.info('Get invited customers started')

        invited_customers = self._get_invited_customers()
        sorted_invited_customers = sorted(invited_customers, key=lambda x: x['user_id'])

        customers_log.info('Result: {}'.format(sorted_invited_customers))
        self._print_invited_customers(sorted_invited_customers)


if __name__ == '__main__':
    InvitedCustomers().get()
