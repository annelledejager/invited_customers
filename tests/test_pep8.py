import unittest
import pycodestyle


class Pep8TestCase(unittest.TestCase):
    defaults = {
        'exclude': ['virtualenv'],
        'ignore': ['E501'],
        'repeat': True,
    }

    def test_pep8(self):
        kwargs = self.defaults.copy()
        style = pycodestyle.StyleGuide(**kwargs)
        report = style.check_files(paths=['../'])
        self.assertEqual(report.total_errors, 0, msg=report)
