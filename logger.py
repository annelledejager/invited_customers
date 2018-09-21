import logging


logging.basicConfig(filename='invited_customers.log', level=logging.DEBUG, format='%(asctime)s %(message)s')

customers_log = logging.getLogger('invited_customers')
