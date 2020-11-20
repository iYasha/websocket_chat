"""
Тесты для чата
"""
import unittest

from utility import get_connection


class TestDatabaseCase(unittest.TestCase):

    def test_connection(self):
        self.assertTrue(get_connection())

    def test_logging(self):
        import logging.config
        logging.config.fileConfig('log.conf')
        logger = logging.getLogger('main')
        self.assertTrue(True)


if __name__ == "__main__":
    unittest.main()
