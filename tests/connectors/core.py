"""
Tests for core connector logic.
"""

# System Imports.
import unittest

# User Imports.
from config import mysql_config, sqlite_config
from src.connectors import MySqlConnector, SqliteConnector
from src.connectors.core import BaseValidate


class TestConnectorCoreTables(unittest.TestCase):
    """
    Tests table connection logic.
    """
    @classmethod
    def setUpClass(cls):
        # Run parent setup logic.
        super().setUpClass()

        cls.test_database_name = 'python__db_connector__mysql_unittest__{0}'.format(cls.__name__)

        # Initialize db connection objects.
        cls.mysql_connector = MySqlConnector(
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


class TestConnectorCoreValidate(unittest.TestCase):
    """
    Tests validation logic.
    """
    @classmethod
    def setUpClass(cls):
        # Run parent setup logic.
        super().setUpClass()

        # Initialize validator class.
        cls.validate = BaseValidate(None)

    def test_validate_database_name(self):
        """
        Tests database name validation logic.
        """
        # For now, always returns true.
        self.assertTrue(self.validate.database_name(None))

    def test_validate_table_name(self):
        """
        Tests table name validation logic.
        """
        # For now, always returns true.
        self.assertTrue(self.validate.table_name(None))

    def test_validate_columns__invalid_type(self):
        """
        Tests column validation logic, using invalid type.
        """
        with self.subTest('With None type'):
            with self.assertRaises(TypeError):
                self.validate.table_columns(None)

        with self.subTest('With int type'):
            with self.assertRaises(TypeError):
                self.validate.table_columns(1)

        with self.subTest('With list type'):
            with self.assertRaises(TypeError):
                self.validate.table_columns(['id INT'])

        with self.subTest('With tuple type'):
            with self.assertRaises(TypeError):
                self.validate.table_columns(('id INT',))

    def test_validate_columns__str(self):
        """
        Tests column validation logic, using str object.
        """
        with self.subTest('Minimal value'):
            self.assertEqual(
                self.validate.table_columns('id INT'),
                '( id INT )',
            )

        with self.subTest('Multi-value'):
            self.assertEqual(
                self.validate.table_columns(
                    'id INT NOT NULL AUTO_INCREMENT, '
                    'title VARCHAR(100) NOT NULL, '
                    'description VARCHAR(255) NOT NULL'
                ),
                '( '
                'id INT NOT NULL AUTO_INCREMENT, '
                'title VARCHAR(100) NOT NULL, '
                'description VARCHAR(255) NOT NULL '
                ')'
            )

        with self.subTest('With bad value'):
            with self.assertRaises(ValueError):
                self.validate.table_columns('id INT;')

    def test_validate_columns__dict(self):
        """
        Tests column validation logic, using dict object.
        """
        with self.subTest('Minimal value'):
            self.assertEqual(
                self.validate.table_columns({'id': 'INT'}),
                '( id INT )',
            )

        with self.subTest('Multi-value'):
            self.assertEqual(
                self.validate.table_columns({
                    'id': 'INT NOT NULL AUTO_INCREMENT',
                    'title': 'VARCHAR(100) NOT NULL',
                    'description': 'VARCHAR(255) NOT NULL',
                }),
                '( '
                'id INT NOT NULL AUTO_INCREMENT, '
                'title VARCHAR(100) NOT NULL, '
                'description VARCHAR(255) NOT NULL '
                ')'
            )

        with self.subTest('With bad key'):
            with self.assertRaises(ValueError):
                self.validate.table_columns({'id;': 'INT'})

        with self.subTest('With bad value'):
            with self.assertRaises(ValueError):
                self.validate.table_columns({'id': 'INT;'})
