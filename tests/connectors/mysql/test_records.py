"""
Tests for "records" logic of "MySQL" DB Connector class.
"""

# System Imports.
import textwrap

# Internal Imports.
from .constants import COLUMNS_CLAUSE__BASIC, COLUMNS_CLAUSE__DATETIME
from .test_core import TestMysqlDatabaseParent
from tests.connectors.core.test_records import CoreRecordsTestMixin


class TestMysqlRecords(TestMysqlDatabaseParent, CoreRecordsTestMixin):
    """
    Tests "MySQL" DB Connector class record logic.
    """
    @classmethod
    def setUpClass(cls):
        # Run parent setup logic.
        super().setUpClass()

        # Also call CoreTestMixin setup logic.
        cls.set_up_class()

        # Define database name to use in tests.
        cls.test_db_name = '{0}test_records'.format(cls.test_db_name_start)

        # Initialize database for tests.
        cls.connector.database.create(cls.test_db_name)
        cls.connector.database.use(cls.test_db_name)

        # Check that database has no tables.
        results = cls.connector.tables.show()
        if len(results) > 0:
            for result in results:
                cls.connector.tables.drop(result)

        # Define default table columns.
        cls._columns_clause__basic = COLUMNS_CLAUSE__BASIC
        cls._columns_clause__datetime = COLUMNS_CLAUSE__DATETIME

        cls.error_handler__table_already_exists = cls.db_error_handler.OperationalError

    def test_error_catch_types(self):
        """Tests to ensure database ERROR types are properly caught.

        Ex: MySQL and PostgreSQL interfaces do not catch "Database does not exist" errors the same.
            These tests make sure this error (and others) are properly caught, regardless of what database is
            being called.
        """
        # Call parent logic.
        super().test_error_catch_types()

        with self.subTest('Verify handling when database already exists'):
            # Make sure we're using a table name that is not already created.
            table_name = 'test_table'
            self.connector.tables.create(table_name, self._columns_clause__basic)

            results = self.connector.tables.show()
            if table_name not in results:
                raise AssertionError('Table not yet present. Incorrect name provided.')

            # Check that we use the correct handler.
            with self.assertRaises(self.error_handler__table_already_exists):
                self.connector.query.execute('CREATE TABLE {0} {1};'.format(table_name, self._columns_clause__basic))
