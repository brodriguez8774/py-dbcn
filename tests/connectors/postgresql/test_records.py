"""
Tests for "records" logic of "PostgreSQL" DB Connector class.
"""

# System Imports.
from decimal import Decimal

# Internal Imports.
from .constants import COLUMNS_CLAUSE__BASIC, COLUMNS_CLAUSE__DATETIME, COLUMNS_CLAUSE__AGGREGATES
from .test_core import TestPostgresqlDatabaseParent
from tests.connectors.core.test_records import CoreRecordsTestMixin


class TestPostgresqlRecords(TestPostgresqlDatabaseParent, CoreRecordsTestMixin):
    """
    Tests "PostgreSQL" DB Connector class record logic.
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
        cls._columns_clause__aggregates = COLUMNS_CLAUSE__AGGREGATES

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
            with self.assertRaises(self.connector.errors.table_already_exists):
                self.connector.query.execute('CREATE TABLE {0} {1};'.format(table_name, self._columns_clause__basic))

    def test__select__aggregates(self):
        """"""
        table_name = 'test_queries__select__aggregate'

        # Run parent tests.
        super().test__select__aggregates()

        # Tests that require slightly different syntax in different database types.
        with self.subTest('SELECT with BIT_OR aggregation'):
            # Run test query.
            results = self.connector.records.select(table_name, 'BIT_OR(test_bool::int)')

            # Verify return aggregate result.
            # No records returned True, so should be False.
            self.assertEqual(len(results), 1)
            self.assertEqual(results[0][0], False)

            # Upset a single record to be true, and test again.
            results = self.connector.records.update(table_name, 'test_bool = True', where_clause='WHERE id = 2')
            results = self.connector.records.select(table_name, 'BIT_OR(test_bool::int)')

            # Verify return aggregate result.
            # At least one record returned True so should be True.
            self.assertEqual(len(results), 1)
            self.assertEqual(results[0][0], True)

        with self.subTest('SELECT with BIT_AND aggregation'):
            # Run test query.
            results = self.connector.records.select(table_name, 'BIT_AND(test_bool::int)')

            # Verify return aggregate result.
            # Not all records returned True, so should be False.
            self.assertEqual(len(results), 1)
            self.assertEqual(results[0][0], False)

            # Update all records to be true, and test again.
            results = self.connector.records.update(table_name, 'test_bool = True', where_clause='')
            results = self.connector.records.select(table_name, 'bit_or(test_bool::int)')

            # Verify return aggregate result.
            # All records returned True so should be True.
            self.assertEqual(len(results), 1)
            self.assertEqual(results[0][0], True)

            # Reset booleans to be False.
            self.connector.records.update(table_name, 'test_bool = False', where_clause='')

        with self.subTest('SELECT with STDDEV aggregation'):
            # Run test query.
            results = self.connector.records.select(table_name, 'STDDEV(test_int)')

            # Verify return aggregate result.
            self.assertEqual(len(results), 1)
            self.assertEqual(results[0][0], Decimal('7.4363969770312827'))

        with self.subTest('SELECT with VARIANCE aggregation'):
            # Run test query.
            results = self.connector.records.select(table_name, 'VARIANCE(test_int)')

            # Verify return aggregate result.
            self.assertEqual(len(results), 1)
            self.assertEqual(results[0][0], Decimal('55.3'))

        # Aggregate functions that don't exist outside of PostgreSQL.
        with self.subTest('SELECT with BOOL_OR aggregation'):
            # Run test query.
            results = self.connector.records.select(table_name, 'BOOL_OR(test_bool)')

            # Verify return aggregate result.
            # No records returned True, so should be False.
            self.assertEqual(len(results), 1)
            self.assertEqual(results[0][0], False)

            # Upset a single record to be true, and test again.
            results = self.connector.records.update(table_name, 'test_bool = True', where_clause='WHERE id = 2')
            results = self.connector.records.select(table_name, 'BOOL_OR(test_bool)')

            # Verify return aggregate result.
            # At least one record returned True so should be True.
            self.assertEqual(len(results), 1)
            self.assertEqual(results[0][0], True)

        with self.subTest('SELECT with BOOL_AND aggregation'):
            # Run test query.
            results = self.connector.records.select(table_name, 'BOOL_AND(test_bool)')

            # Verify return aggregate result.
            # Not all records returned True, so should be False.
            self.assertEqual(len(results), 1)
            self.assertEqual(results[0][0], False)

            # Update all records to be true, and test again.
            self.connector.records.update(table_name, 'test_bool = True', where_clause='')
            results = self.connector.records.select(table_name, 'BOOL_or(test_bool)')

            # Verify return aggregate result.
            # All records returned True so should be True.
            self.assertEqual(len(results), 1)
            self.assertEqual(results[0][0], True)

            # Reset booleans to be False.
            self.connector.records.update(table_name, 'test_bool = False', where_clause='')
