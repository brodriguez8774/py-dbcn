"""
Tests for "validate" logic of "Core" DB Connector class.
"""

# System Imports.
import unittest

# User Imports.
from config import mysql_config, sqlite_config
from src.connectors import MysqlDbConnector, PostgresqlDbConnector, SqliteDbConnector
from src.connectors.core.validate import BaseValidate


class TestCoreValidate(unittest.TestCase):
    """
    Tests "Core" DB Connector class validation logic.
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
