"""
Tests for "tables" logic of "Core" DB Connector class.
"""

# System Imports.
import unittest

# User Imports.
from config import mysql_config, sqlite_config
from src.connectors import MysqlDbConnector, PostgresqlDbConnector, SqliteDbConnector


class TestCoreTables(unittest.TestCase):
    """
    Tests "Core" DB Connector class table logic.
    """
    @classmethod
    def setUpClass(cls):
        # Run parent setup logic.
        super().setUpClass()

        cls.test_database_name = 'python__db_connector__mysql_unittest__{0}'.format(cls.__name__)

        # Initialize db connection objects.
        cls.mysql_connector = MysqlDbConnector(
            mysql_config['host'],
            mysql_config['port'],
            mysql_config['user'],
            mysql_config['password'],
            mysql_config['name'],
            debug=True,
        )

        # Check that expected database exists.
        results = cls.mysql_connector.database.show()
        if cls.test_database_name not in results:
            cls.mysql_connector.database.create(cls.test_database_name)
            print('Created database "{0}".'.format(cls.test_database_name))

        # Select desired database for usage.
        cls.mysql_connector.database.use(cls.test_database_name)

        # Check that database has no tables.
        results = cls.mysql_connector.tables.show()
        if len(results) > 0:
            for result in results:
                print('Clearing existing tables for "{0}".'.format(cls.test_database_name))
                cls.mysql_connector.tables.drop(result)

    @classmethod
    def tearDownClass(cls):
        # Run parent setup logic.
        super().tearDownClass()

        # Remove expected database.
        cls.mysql_connector.database.drop(cls.test_database_name)

    def setUp(self):
        # Run parent setup logic.
        super().setUp()

    def test__create_table___col_str(self):
        """
        Tests that connector object properly creates new tables, via str of column data.
        """
        table_name = 'test_create_table'

        # Check that expected table DOES NOT yet exist in database.
        results = self.mysql_connector.tables.show()
        self.assertNotIn(table_name, results)

        # Attempt to generate table.
        self.mysql_connector.tables.create(table_name, 'id INT(11) NOT NULL AUTO_INCREMENT, PRIMARY KEY (id)')

        # Check that expected table now exists in database.
        results = self.mysql_connector.tables.show()
        self.assertIn(table_name, results)

    # def test__create_table___col_dict(self):
    #     """
    #     Tests that connector object properly creates new tables, via dict of column data.
    #     """
    #     table_name = 'test_create_table'
    #
    #     # Check that expected table DOES NOT yet exist in database.
    #     results = self.mysql_connector.tables.show()
    #     self.assertNotIn(table_name, results)
    #
    #     # Attempt to generate table.
    #     self.mysql_connector.tables.create(table_name, 'id INT(11) NOT NULL AUTO_INCREMENT, PRIMARY KEY (id)')
    #
    #     # Check that expected table now exists in database.
    #     results = self.mysql_connector.tables.show()
    #     self.assertIn(table_name, results)

    def test__drop_table(self):
        """
        Tests that connector object properly drops tables.
        """
        table_name = 'test_drop_table'

        # Check that expected table DOES NOT yet exist in database.
        results = self.mysql_connector.tables.show()
        self.assertNotIn(table_name, results)

        # Attempt to generate table.
        self.mysql_connector.tables.create(table_name, 'id INT(11) NOT NULL AUTO_INCREMENT, PRIMARY KEY (id)')

        # Check that expected table now exists in database.
        results = self.mysql_connector.tables.show()
        self.assertIn(table_name, results)

        # Attempt to remove table.
        self.mysql_connector.tables.drop(table_name)

        # Check that expected table was removed.
        results = self.mysql_connector.tables.show()
        self.assertNotIn(table_name, results)
