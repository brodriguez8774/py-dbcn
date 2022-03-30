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
