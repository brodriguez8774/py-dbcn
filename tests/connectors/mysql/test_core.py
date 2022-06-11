"""
Tests for "core" logic of "MySQL" DB Connector class.
"""

# System Imports.
import unittest

# User Imports.
from config import mysql_config
from src.connectors import MysqlDbConnector


class TestMysqlDatabaseParent(unittest.TestCase):
    """
    Tests "MySQL" DB Connector class database logic.
    """
    @classmethod
    def setUpClass(cls):
        # Run parent setup logic.
        super().setUpClass()

        # Initialize connector class to test.
        cls.connector = MysqlDbConnector(
            mysql_config['host'],
            mysql_config['port'],
            mysql_config['user'],
            mysql_config['password'],
            mysql_config['name'],
            debug=True,
        )

    @classmethod
    def tearDownClass(cls):
        # Destroy all leftover databases created during tests.
        results = cls.connector.database.show()
        for result in results:
            if result.startswith('python__db_connector__test'):
                cls.connector.database.drop(result)

        # Run parent teardown logic.
        super().tearDownClass()

    def assertText(self, actual_text, expected_text):
        """Wrapper for assertEquals, that prints values to console on mismatch."""
        actual_text = str(actual_text).strip()
        expected_text = str(expected_text).strip()

        # Attempt assertion.
        try:
            self.assertEqual(actual_text, expected_text)
        except AssertionError as err:
            # Assertion failed. Provide debug output.
            print('\n\n\n\n')
            print('ACTUAL:')
            print(actual_text)
            print('\n')
            print('EXPECTED:')
            print(expected_text)
            print('\n\n\n\n')

            # Raise original error.
            raise AssertionError(err)
