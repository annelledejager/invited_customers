import unittest

from invited_customers.tests.test_pep8 import Pep8TestCase
from invited_customers.tests.test_helpers import GetShortestDistanceBetweenTwoCoordinatesTestCase, ConvertToFloatTestCase
from invited_customers.tests.test_invited_customers import InvitedCustomersTestCase, PrintInvitedCustomerTestCase, \
    FormatCustomerTestCase, GetDistanceFromOfficeTestCase, ParseCustomerTestCase, GetTestCase, \
    GetInvitedCustomerTestCase


def create_suite():
    test_suite = unittest.TestSuite()
    test_suite.addTest(unittest.makeSuite(ConvertToFloatTestCase))
    test_suite.addTest(unittest.makeSuite(FormatCustomerTestCase))
    test_suite.addTest(unittest.makeSuite(GetDistanceFromOfficeTestCase))
    test_suite.addTest(unittest.makeSuite(GetInvitedCustomerTestCase))
    test_suite.addTest(unittest.makeSuite(GetShortestDistanceBetweenTwoCoordinatesTestCase))
    test_suite.addTest(unittest.makeSuite(GetTestCase))
    test_suite.addTest(unittest.makeSuite(InvitedCustomersTestCase))
    test_suite.addTest(unittest.makeSuite(ParseCustomerTestCase))
    test_suite.addTest(unittest.makeSuite(Pep8TestCase))
    test_suite.addTest(unittest.makeSuite(PrintInvitedCustomerTestCase))

    return test_suite


if __name__ == '__main__':
    suite = create_suite()

    runner = unittest.TextTestRunner()
    runner.run(suite)
