"""
Initialization of"records" logic of "Core" DB Connector class.

Note that the tests for the "Core" DB Connector class don't do anything in themselves.
They're meant to define a majority of overall database logic, which is then inherited/tweaked by the
various specific database test classes. This ensures that all databases types run similar/equal tests.
"""

# System Imports.
import datetime
from decimal import Decimal

# Internal Imports.


class CoreRecordsTestMixin:
    """
    Tests "Core" DB Connector class record logic.
    """
    @classmethod
    def set_up_class(cls):
        """
        Acts as the equivalent of the UnitTesting "setUpClass()" function.

        However, since this is not inheriting from a given TestCase,
        calling the literal function here would override instead.
        """
        cls.test_db_name_start = cls.test_db_name_start.format(cls.db_type)

        cls._columns_clause__basic = None
        cls._columns_clause__datetime = None
        cls._columns_clause__aggregates = None

    def test_error_catch_types(self):
        """Tests to ensure database ERROR types are properly caught.

        For example, MySQL and PostgreSQL interfaces do not catch "Database Does Not Exist" errors the same way.
        These tests make sure this error (and others) are properly caught, regardless of what database is being called.
        """
        # Ensure error types are first defined.
        if not self.connector.errors.table_already_exists:
            raise ValueError('Please define error handler for "Table Already Exists" error type.')

    def test__select__success(self):
        """
        Test `SELECT` query.
        """
        table_name = 'test_queries__select__success'

        # Verify table exists.
        try:
            self.connector.query.execute('CREATE TABLE {0}{1};'.format(table_name, self._columns_clause__basic))
        except self.connector.errors.table_already_exists:
            # Table already exists, as we want.
            pass

        with self.subTest('SELECT query when table has no records'):
            # Run test query.
            results = self.connector.records.select(table_name)

            # Verify no records returned.
            self.assertEqual(len(results), 0)

        with self.subTest('SELECT query when table has one record'):
            # Insert record.
            row_1 = (1, 'test_name_1', 'test_desc_1')
            self.connector.query.execute('INSERT INTO {0} VALUES {1};'.format(table_name, row_1))

            # Run test query.
            results = self.connector.records.select(table_name)

            # Verify one record returned.
            self.assertEqual(len(results), 1)
            self.assertIn(row_1, results)

        with self.subTest('SELECT query when table has two records'):
            # Insert record.
            row_2 = (2, 'test_name_2', 'test_desc_2')
            self.connector.query.execute('INSERT INTO {0} VALUES {1};'.format(table_name, row_2))

            # Run test query.
            results = self.connector.records.select(table_name)

            # Verify two records returned.
            self.assertEqual(len(results), 2)
            self.assertIn(row_1, results)
            self.assertIn(row_2, results)

        # Works for 0, 1, and 2. Assume works for all further n+1 values.

        with self.subTest('SELECT query when table record has spaces'):
            # Insert record.
            row_3 = (3, 'test name 3', 'test desc 3')
            self.connector.query.execute('INSERT INTO {0} VALUES {1};'.format(table_name, row_3))

            # Run test query.
            results = self.connector.records.select(table_name)

            # Verify two records returned.
            self.assertEqual(len(results), 3)
            self.assertIn(row_1, results)
            self.assertIn(row_2, results)
            self.assertIn(row_3, results)

        with self.subTest('SELECT query when table column uses "reserved keyword"'):
            # "Group" is considered a SQL keyword. As long as this doesn't raise an error, it worked.
            self.connector.tables.add_column(
                table_name,
                '{0}group{0} VARCHAR(100)'.format(self.connector.validate._quote_identifier_format),
            )
            results = self.connector.records.select(table_name)

            # Verify two records returned, now with an extra "group" field that shows null.
            row_1 = row_1 + (None,)
            row_2 = row_2 + (None,)
            row_3 = row_3 + (None,)
            self.assertEqual(len(results), 3)
            self.assertIn(row_1, results)
            self.assertIn(row_2, results)
            self.assertIn(row_3, results)

    def test__select__with_where__success(self):
        """
        Test `SELECT` query when using where clauses.
        """
        table_name = 'test_queries__select__where__success'

        # Verify table exists.
        try:
            self.connector.query.execute('CREATE TABLE {0}{1};'.format(table_name, self._columns_clause__basic))
        except self.connector.errors.table_already_exists:
            # Table already exists, as we want.
            pass

        with self.subTest('SELECT with WHERE when table has no records'):
            # Run test query.
            results = self.connector.records.select(
                table_name,
                where_clause='description = {0}test aaa{0}'.format(self.connector.validate._quote_str_literal_format),
            )

            # Verify no records returned.
            self.assertEqual(len(results), 0)

        with self.subTest('SELECT with WHERE when table has one unrelated record'):
            # Insert record.
            row_1 = (1, 'test_name_1', 'test_desc_1')
            self.connector.query.execute('INSERT INTO {0} VALUES {1};'.format(table_name, row_1))

            # Run test query.
            results = self.connector.records.select(
                table_name,
                where_clause='description = {0}test aaa{0}'.format(self.connector.validate._quote_str_literal_format)
            )

            # Verify no records returned.
            self.assertEqual(len(results), 0)

        with self.subTest('SELECT with WHERE when table has one unrelated record and one related'):
            # Insert record.
            row_2 = (2, 'test_name_2', 'test aaa')
            self.connector.query.execute('INSERT INTO {0} VALUES {1};'.format(table_name, row_2))

            # Run test query.
            results = self.connector.records.select(
                table_name,
                where_clause='description = {0}test aaa{0}'.format(self.connector.validate._quote_str_literal_format)
            )

            # Verify no records returned.
            self.assertEqual(len(results), 1)
            self.assertIn(row_2, results)
            self.assertNotIn(row_1, results)

        with self.subTest('SELECT with WHERE when table has two unrelated records and one related'):
            # Insert record.
            row_3 = (3, 'test aaa', 'test_desc_3')
            self.connector.query.execute('INSERT INTO {0} VALUES {1};'.format(table_name, row_3))

            # Run test query.
            results = self.connector.records.select(
                table_name,
                where_clause='description = {0}test aaa{0}'.format(self.connector.validate._quote_str_literal_format),
            )

            # Verify no records returned.
            self.assertEqual(len(results), 1)
            self.assertIn(row_2, results)
            self.assertNotIn(row_1, results)
            self.assertNotIn(row_3, results)

        with self.subTest('SELECT with WHERE when table has two unrelated records and two related'):
            # Insert record.
            row_4 = (4, 'test_name_4', 'test aaa')
            self.connector.query.execute('INSERT INTO {0} VALUES {1};'.format(table_name, row_4))

            # Run test query.
            results = self.connector.records.select(
                table_name,
                where_clause='description = {0}test aaa{0}'.format(self.connector.validate._quote_str_literal_format),
            )

            # Verify no records returned.
            self.assertEqual(len(results), 2)
            self.assertIn(row_2, results)
            self.assertIn(row_4, results)
            self.assertNotIn(row_1, results)
            self.assertNotIn(row_3, results)

    def test__select__with_order_by__success__by_one_col(self):
        """
        Test `SELECT` query when using order_by clauses on a single column.
        """
        table_name = 'test_queries__select__order_by__single__success'
        # Verify table exists.
        try:
            self.connector.query.execute('CREATE TABLE {0}{1};'.format(table_name, self._columns_clause__basic))
        except self.connector.errors.table_already_exists:
            # Table already exists, as we want.
            pass

        with self.subTest('SELECT with ORDER BY when table has no records'):
            # Mostly just making sure there are no errors in this case.

            # Run test query.
            results = self.connector.records.select(table_name, order_by_clause='description')

            # Verify records returned in expected order.
            self.assertEqual(len(results), 0)

        # Insert record.
        row_1 = (1, 'test_name_1', 'test_desc_1')
        self.connector.query.execute('INSERT INTO {0} VALUES {1};'.format(table_name, row_1))

        with self.subTest('SELECT with ORDER BY when table has one record'):
            # Mostly just making sure there are no errors in this case.

            # Run test query.
            results = self.connector.records.select(table_name, order_by_clause='description')

            # Verify records returned in expected order.
            self.assertEqual(len(results), 1)
            self.assertEqual(row_1, results[0])

        # Insert record.
        row_2 = (2, 'z name', 'z desc')
        self.connector.query.execute('INSERT INTO {0} VALUES {1};'.format(table_name, row_2))

        with self.subTest('SELECT with ORDER BY when table has two records - By Unspecified'):
            # Run test query.
            results = self.connector.records.select(table_name, order_by_clause='description')

            # Verify records returned in expected order.
            self.assertEqual(len(results), 2)
            self.assertEqual(row_1, results[0])
            self.assertEqual(row_2, results[1])

        with self.subTest('SELECT with ORDER BY when table has two records - By ASC'):
            # Run test query.
            results = self.connector.records.select(table_name, order_by_clause='description ASC')

            # Verify records returned in expected order.
            self.assertEqual(len(results), 2)
            self.assertEqual(row_1, results[0])
            self.assertEqual(row_2, results[1])

        with self.subTest('SELECT with ORDER BY when table has two records - By DESC'):
            # Run test query.
            results = self.connector.records.select(table_name, order_by_clause='description DESC')

            # Verify records returned in expected order.
            self.assertEqual(len(results), 2)
            self.assertEqual(row_2, results[0])
            self.assertEqual(row_1, results[1])

        # Insert record.
        row_3 = (3, 'a name', 'a desc')
        self.connector.query.execute('INSERT INTO {0} VALUES {1};'.format(table_name, row_3))

        with self.subTest('SELECT with ORDER BY when table has three records - By Unspecified'):
            # Run test query.
            results = self.connector.records.select(table_name, order_by_clause='description')

            # Verify records returned in expected order.
            self.assertEqual(len(results), 3)
            self.assertEqual(row_3, results[0])
            self.assertEqual(row_1, results[1])
            self.assertEqual(row_2, results[2])

        with self.subTest('SELECT with ORDER BY when table has three records - By ASC'):
            # Run test query.
            results = self.connector.records.select(table_name, order_by_clause='description ASC')

            # Verify records returned in expected order.
            self.assertEqual(len(results), 3)
            self.assertEqual(row_3, results[0])
            self.assertEqual(row_1, results[1])
            self.assertEqual(row_2, results[2])

        with self.subTest('SELECT with ORDER BY when table has three records - By DESC'):
            # Run test query.
            results = self.connector.records.select(table_name, order_by_clause='description DESC')

            # Verify records returned in expected order.
            self.assertEqual(len(results), 3)
            self.assertEqual(row_2, results[0])
            self.assertEqual(row_1, results[1])
            self.assertEqual(row_3, results[2])

        # Insert record.
        row_4 = (4, 'the name', 'the desc')
        self.connector.query.execute('INSERT INTO {0} VALUES {1};'.format(table_name, row_4))

        with self.subTest('SELECT with ORDER BY when table has four records - By Unspecified'):
            # Run test query.
            results = self.connector.records.select(table_name, order_by_clause='description')

            # Verify records returned in expected order.
            self.assertEqual(len(results), 4)
            self.assertEqual(row_3, results[0])
            self.assertEqual(row_1, results[1])
            self.assertEqual(row_4, results[2])
            self.assertEqual(row_2, results[3])

        with self.subTest('SELECT with ORDER BY when table has four records - By ASC'):
            # Run test query.
            results = self.connector.records.select(table_name, order_by_clause='description ASC')

            # Verify records returned in expected order.
            self.assertEqual(len(results), 4)
            self.assertEqual(row_3, results[0])
            self.assertEqual(row_1, results[1])
            self.assertEqual(row_4, results[2])
            self.assertEqual(row_2, results[3])

        with self.subTest('SELECT with ORDER BY when table has four records - By DESC'):
            # Run test query.
            results = self.connector.records.select(table_name, order_by_clause='description DESC')

            # Verify records returned in expected order.
            self.assertEqual(len(results), 4)
            self.assertEqual(row_2, results[0])
            self.assertEqual(row_4, results[1])
            self.assertEqual(row_1, results[2])
            self.assertEqual(row_3, results[3])

        # Insert record.
        row_5 = (5, 'b name', 'b desc')
        self.connector.query.execute('INSERT INTO {0} VALUES {1};'.format(table_name, row_5))

        with self.subTest('SELECT with ORDER BY when table has five records - By Unspecified'):
            # Run test query.
            results = self.connector.records.select(table_name, order_by_clause='description')

            # Verify records returned in expected order.
            self.assertEqual(len(results), 5)
            self.assertEqual(row_3, results[0])
            self.assertEqual(row_5, results[1])
            self.assertEqual(row_1, results[2])
            self.assertEqual(row_4, results[3])
            self.assertEqual(row_2, results[4])

        with self.subTest('SELECT with ORDER BY when table has five records - By ASC'):
            # Run test query.
            results = self.connector.records.select(table_name, order_by_clause='description ASC')

            # Verify records returned in expected order.
            self.assertEqual(len(results), 5)
            self.assertEqual(row_3, results[0])
            self.assertEqual(row_5, results[1])
            self.assertEqual(row_1, results[2])
            self.assertEqual(row_4, results[3])
            self.assertEqual(row_2, results[4])

        with self.subTest('SELECT with ORDER BY when table has five records - By DESC'):
            # Run test query.
            results = self.connector.records.select(table_name, order_by_clause='description DESC')

            # Verify records returned in expected order.
            self.assertEqual(len(results), 5)
            self.assertEqual(row_2, results[0])
            self.assertEqual(row_4, results[1])
            self.assertEqual(row_1, results[2])
            self.assertEqual(row_5, results[3])
            self.assertEqual(row_3, results[4])

    def test__select__with_order_by__success__by_multiple_cols(self):
        """
        Test `SELECT` query when using order_by clauses on multiple column.
        """
        table_name = 'test_queries__select__order_by__multiple__success'
        # Verify table exists.
        try:
            self.connector.query.execute('CREATE TABLE {0}{1};'.format(table_name, self._columns_clause__basic))
        except self.connector.errors.table_already_exists:
            # Table already exists, as we want.
            pass

        with self.subTest('SELECT with ORDER BY when table has no records'):
            # Mostly just making sure there are no errors in this case.

            # Run test query.
            results = self.connector.records.select(table_name, order_by_clause='description, name')

            # Verify records returned in expected order.
            self.assertEqual(len(results), 0)

        # Insert records.
        row_1 = (1, 'test_name_1', 'test_desc_1')
        self.connector.query.execute('INSERT INTO {0} VALUES {1};'.format(table_name, row_1))
        row_2 = (2, 'This is a test name', 'Some desc')
        self.connector.query.execute('INSERT INTO {0} VALUES {1};'.format(table_name, row_2))
        row_3 = (3, 'aaa name', 'zzz desc')
        self.connector.query.execute('INSERT INTO {0} VALUES {1};'.format(table_name, row_3))
        row_4 = (4, 'zzz name', 'This is a test description')
        self.connector.query.execute('INSERT INTO {0} VALUES {1};'.format(table_name, row_4))
        row_5 = (5, 'some name', 'aaa desc')
        self.connector.query.execute('INSERT INTO {0} VALUES {1};'.format(table_name, row_5))
        row_6 = (6, 'test_name_1', 'test_desc_1')
        self.connector.query.execute('INSERT INTO {0} VALUES {1};'.format(table_name, row_6))
        # Duplicate records in all but pk. Guarantees there is multiple overlap with ordering fields.
        row_7 = (7, 'test_name_1', 'test_desc_1')
        self.connector.query.execute('INSERT INTO {0} VALUES {1};'.format(table_name, row_7))
        row_8 = (8, 'This is a test name', 'Some desc')
        self.connector.query.execute('INSERT INTO {0} VALUES {1};'.format(table_name, row_8))
        row_9 = (9, 'aaa name', 'zzz desc')
        self.connector.query.execute('INSERT INTO {0} VALUES {1};'.format(table_name, row_9))
        row_10 = (10, 'zzz name', 'This is a test description')
        self.connector.query.execute('INSERT INTO {0} VALUES {1};'.format(table_name, row_10))
        row_11 = (11, 'some name', 'aaa desc')
        self.connector.query.execute('INSERT INTO {0} VALUES {1};'.format(table_name, row_11))
        row_12 = (12, 'test_name_1', 'test_desc_1')
        self.connector.query.execute('INSERT INTO {0} VALUES {1};'.format(table_name, row_12))

        with self.subTest('SELECT with ORDER BY - By name, id - ASC'):
            # Run test query.
            results = self.connector.records.select(table_name, order_by_clause='name, id')

            # Verify records returned in expected order.
            self.assertEqual(len(results), 12)
            self.assertEqual(row_3, results[0])
            self.assertEqual(row_9, results[1])
            self.assertEqual(row_5, results[2])
            self.assertEqual(row_11, results[3])
            self.assertEqual(row_1, results[4])
            self.assertEqual(row_6, results[5])
            self.assertEqual(row_7, results[6])
            self.assertEqual(row_12, results[7])
            self.assertEqual(row_2, results[8])
            self.assertEqual(row_8, results[9])
            self.assertEqual(row_4, results[10])
            self.assertEqual(row_10, results[11])

        with self.subTest('SELECT with ORDER BY - By name, id - DESC'):
            # Run test query.
            results = self.connector.records.select(table_name, order_by_clause='name DESC, id DESC')

            # Verify records returned in expected order.
            self.assertEqual(len(results), 12)
            self.assertEqual(row_10, results[0])
            self.assertEqual(row_4, results[1])
            self.assertEqual(row_8, results[2])
            self.assertEqual(row_2, results[3])
            self.assertEqual(row_12, results[4])
            self.assertEqual(row_7, results[5])
            self.assertEqual(row_6, results[6])
            self.assertEqual(row_1, results[7])
            self.assertEqual(row_11, results[8])
            self.assertEqual(row_5, results[9])
            self.assertEqual(row_9, results[10])
            self.assertEqual(row_3, results[11])

        with self.subTest('SELECT with ORDER BY - By name, id - MIXED'):
            # Run test query.
            results = self.connector.records.select(table_name, order_by_clause='name DESC, id ASC')

            # Verify records returned in expected order.
            self.assertEqual(len(results), 12)
            self.assertEqual(row_4, results[0])
            self.assertEqual(row_10, results[1])
            self.assertEqual(row_2, results[2])
            self.assertEqual(row_8, results[3])
            self.assertEqual(row_1, results[4])
            self.assertEqual(row_6, results[5])
            self.assertEqual(row_7, results[6])
            self.assertEqual(row_12, results[7])
            self.assertEqual(row_5, results[8])
            self.assertEqual(row_11, results[9])
            self.assertEqual(row_3, results[10])
            self.assertEqual(row_9, results[11])

        with self.subTest('SELECT with ORDER BY - By description, id - ASC'):
            # Run test query.
            results = self.connector.records.select(table_name, order_by_clause='description, id')

            # Verify records returned in expected order.
            self.assertEqual(len(results), 12)
            self.assertEqual(row_5, results[0])
            self.assertEqual(row_11, results[1])
            self.assertEqual(row_2, results[2])
            self.assertEqual(row_8, results[3])
            self.assertEqual(row_1, results[4])
            self.assertEqual(row_6, results[5])
            self.assertEqual(row_7, results[6])
            self.assertEqual(row_12, results[7])
            self.assertEqual(row_4, results[8])
            self.assertEqual(row_10, results[9])
            self.assertEqual(row_3, results[10])
            self.assertEqual(row_9, results[11])

        with self.subTest('SELECT with ORDER BY - By description, id - DESC'):
            # Run test query.
            results = self.connector.records.select(table_name, order_by_clause='description DESC, id DESC')

            # Verify records returned in expected order.
            self.assertEqual(len(results), 12)
            self.assertEqual(row_9, results[0])
            self.assertEqual(row_3, results[1])
            self.assertEqual(row_10, results[2])
            self.assertEqual(row_4, results[3])
            self.assertEqual(row_12, results[4])
            self.assertEqual(row_7, results[5])
            self.assertEqual(row_6, results[6])
            self.assertEqual(row_1, results[7])
            self.assertEqual(row_8, results[8])
            self.assertEqual(row_2, results[9])
            self.assertEqual(row_11, results[10])
            self.assertEqual(row_5, results[11])

        with self.subTest('SELECT with ORDER BY - By description, id - MIXED'):
            # Run test query.
            results = self.connector.records.select(table_name, order_by_clause='description DESC, id ASC')

            # Verify records returned in expected order.
            self.assertEqual(len(results), 12)
            self.assertEqual(row_3, results[0])
            self.assertEqual(row_9, results[1])
            self.assertEqual(row_4, results[2])
            self.assertEqual(row_10, results[3])
            self.assertEqual(row_1, results[4])
            self.assertEqual(row_6, results[5])
            self.assertEqual(row_7, results[6])
            self.assertEqual(row_12, results[7])
            self.assertEqual(row_2, results[8])
            self.assertEqual(row_8, results[9])
            self.assertEqual(row_5, results[10])
            self.assertEqual(row_11, results[11])

        with self.subTest('SELECT with ORDER BY - By id, name, description - ASC'):
            # Run test query.
            results = self.connector.records.select(table_name, order_by_clause='id, name, description')

            # Verify records returned in expected order.
            self.assertEqual(len(results), 12)
            self.assertEqual(row_1, results[0])
            self.assertEqual(row_2, results[1])
            self.assertEqual(row_3, results[2])
            self.assertEqual(row_4, results[3])
            self.assertEqual(row_5, results[4])
            self.assertEqual(row_6, results[5])
            self.assertEqual(row_7, results[6])
            self.assertEqual(row_8, results[7])
            self.assertEqual(row_9, results[8])
            self.assertEqual(row_10, results[9])
            self.assertEqual(row_11, results[10])
            self.assertEqual(row_12, results[11])

        with self.subTest('SELECT with ORDER BY - By id, name, description - DESC'):
            # Run test query.
            results = self.connector.records.select(table_name, order_by_clause='id DESC, name DESC, description DESC')

            # Verify records returned in expected order.
            self.assertEqual(len(results), 12)
            self.assertEqual(row_12, results[0])
            self.assertEqual(row_11, results[1])
            self.assertEqual(row_10, results[2])
            self.assertEqual(row_9, results[3])
            self.assertEqual(row_8, results[4])
            self.assertEqual(row_7, results[5])
            self.assertEqual(row_6, results[6])
            self.assertEqual(row_5, results[7])
            self.assertEqual(row_4, results[8])
            self.assertEqual(row_3, results[9])
            self.assertEqual(row_2, results[10])
            self.assertEqual(row_1, results[11])

        with self.subTest('SELECT with ORDER BY - By name, description, id - ASC'):
            # Run test query.
            results = self.connector.records.select(table_name, order_by_clause='name ASC, description ASC, id ASC')

            # Verify records returned in expected order.
            self.assertEqual(len(results), 12)
            self.assertEqual(row_3, results[0])
            self.assertEqual(row_9, results[1])
            self.assertEqual(row_5, results[2])
            self.assertEqual(row_11, results[3])
            self.assertEqual(row_1, results[4])
            self.assertEqual(row_6, results[5])
            self.assertEqual(row_7, results[6])
            self.assertEqual(row_12, results[7])
            self.assertEqual(row_2, results[8])
            self.assertEqual(row_8, results[9])
            self.assertEqual(row_4, results[10])
            self.assertEqual(row_10, results[11])

        with self.subTest('SELECT with ORDER BY - By name, description, id - DESC'):
            # Run test query.
            results = self.connector.records.select(table_name, order_by_clause='name DESC, description DESC, id DESC')

            # Verify records returned in expected order.
            self.assertEqual(len(results), 12)
            self.assertEqual(row_10, results[0])
            self.assertEqual(row_4, results[1])
            self.assertEqual(row_8, results[2])
            self.assertEqual(row_2, results[3])
            self.assertEqual(row_12, results[4])
            self.assertEqual(row_7, results[5])
            self.assertEqual(row_6, results[6])
            self.assertEqual(row_1, results[7])
            self.assertEqual(row_11, results[8])
            self.assertEqual(row_5, results[9])
            self.assertEqual(row_9, results[10])
            self.assertEqual(row_3, results[11])

        with self.subTest('SELECT with ORDER BY - By description, name, id - ASC'):
            # Run test query.
            results = self.connector.records.select(table_name, order_by_clause='description ASC, name ASC, id ASC')

            # Verify records returned in expected order.
            self.assertEqual(len(results), 12)
            self.assertEqual(row_5, results[0])
            self.assertEqual(row_11, results[1])
            self.assertEqual(row_2, results[2])
            self.assertEqual(row_8, results[3])
            self.assertEqual(row_1, results[4])
            self.assertEqual(row_6, results[5])
            self.assertEqual(row_7, results[6])
            self.assertEqual(row_12, results[7])
            self.assertEqual(row_4, results[8])
            self.assertEqual(row_10, results[9])
            self.assertEqual(row_3, results[10])
            self.assertEqual(row_9, results[11])

        with self.subTest('SELECT with ORDER BY - By description, name, id - DESC'):
            # Run test query.
            results = self.connector.records.select(table_name, order_by_clause='description DESC, name DESC, id DESC')

            # Verify records returned in expected order.
            self.assertEqual(len(results), 12)
            self.assertEqual(row_9, results[0])
            self.assertEqual(row_3, results[1])
            self.assertEqual(row_10, results[2])
            self.assertEqual(row_4, results[3])
            self.assertEqual(row_12, results[4])
            self.assertEqual(row_7, results[5])
            self.assertEqual(row_6, results[6])
            self.assertEqual(row_1, results[7])
            self.assertEqual(row_8, results[8])
            self.assertEqual(row_2, results[9])
            self.assertEqual(row_11, results[10])
            self.assertEqual(row_5, results[11])

    def test__select__with_limit__success(self):
        """
        Test `SELECT` query when using limit clauses.
        """
        table_name = 'test_queries__select__limit__success'

        # Verify table exists.
        try:
            self.connector.query.execute('CREATE TABLE {0}{1};'.format(table_name, self._columns_clause__basic))
        except self.connector.errors.table_already_exists:
            # Table already exists, as we want.
            pass

        with self.subTest('SELECT with LIMIT when table has no records'):
            # Run test query.
            results = self.connector.records.select(
                table_name,
                limit_clause=5,
            )

            # Verify no records returned.
            self.assertEqual(len(results), 0)

        with self.subTest('SELECT with LIMIT when table has less records than limit'):
            # Insert record.
            row_1 = (1, 'test_name_1', 'test_desc_1')
            self.connector.query.execute('INSERT INTO {0} VALUES {1};'.format(table_name, row_1))
            row_2 = (2, 'test_name_2', 'test_desc_2')
            self.connector.query.execute('INSERT INTO {0} VALUES {1};'.format(table_name, row_2))
            row_3 = (3, 'test_name_3', 'test_desc_3')
            self.connector.query.execute('INSERT INTO {0} VALUES {1};'.format(table_name, row_3))
            row_4 = (4, 'test_name_4', 'test_desc_4')
            self.connector.query.execute('INSERT INTO {0} VALUES {1};'.format(table_name, row_4))

            # Run test query.
            results = self.connector.records.select(
                table_name,
                limit_clause=5,
            )

            # Verify all records returned.
            self.assertEqual(len(results), 4)
            self.assertIn(row_1, results)
            self.assertIn(row_2, results)
            self.assertIn(row_3, results)
            self.assertIn(row_4, results)

        with self.subTest('SELECT with LIMIT when table has equal records to limit'):
            # Insert record.
            row_5 = (5, 'test_name_5', 'test_desc_5')
            self.connector.query.execute('INSERT INTO {0} VALUES {1};'.format(table_name, row_5))

            # Run test query.
            results = self.connector.records.select(
                table_name,
                limit_clause=5,
            )

            # Verify all records returned.
            self.assertEqual(len(results), 5)
            self.assertIn(row_1, results)
            self.assertIn(row_2, results)
            self.assertIn(row_3, results)
            self.assertIn(row_4, results)
            self.assertIn(row_5, results)

        with self.subTest('SELECT with LIMIT when table has more records than limit'):
            # Insert record.
            row_6 = (6, 'test_name_6', 'test_desc_6')
            self.connector.query.execute('INSERT INTO {0} VALUES {1};'.format(table_name, row_6))

            # Verify table has 6 total records.
            results = self.connector.records.select(table_name)
            self.assertEqual(len(results), 6)

            # Run test query.
            results = self.connector.records.select(
                table_name,
                limit_clause=5,
            )

            # Verify limited set of records returned.
            self.assertEqual(len(results), 5)
            self.assertIn(row_1, results)
            self.assertIn(row_2, results)
            self.assertIn(row_3, results)
            self.assertIn(row_4, results)
            self.assertIn(row_5, results)

        with self.subTest('SELECT with LIMIT when table has many more records than limit'):
            # Insert record.
            row_7 = (7, 'test_name_7', 'test_desc_7')
            self.connector.query.execute('INSERT INTO {0} VALUES {1};'.format(table_name, row_7))
            row_8 = (8, 'test_name_8', 'test_desc_8')
            self.connector.query.execute('INSERT INTO {0} VALUES {1};'.format(table_name, row_8))
            row_9 = (9, 'test_name_9', 'test_desc_9')
            self.connector.query.execute('INSERT INTO {0} VALUES {1};'.format(table_name, row_9))
            row_10 = (10, 'test_name_10', 'test_desc_10')
            self.connector.query.execute('INSERT INTO {0} VALUES {1};'.format(table_name, row_10))
            row_11 = (11, 'test_name_11', 'test_desc_11')
            self.connector.query.execute('INSERT INTO {0} VALUES {1};'.format(table_name, row_11))

            # Verify table has 11 total records.
            results = self.connector.records.select(table_name)
            self.assertEqual(len(results), 11)

            # Run test query.
            results = self.connector.records.select(
                table_name,
                limit_clause=5,
            )

            # Verify limited set of records returned.
            self.assertEqual(len(results), 5)
            self.assertIn(row_1, results)
            self.assertIn(row_2, results)
            self.assertIn(row_3, results)
            self.assertIn(row_4, results)
            self.assertIn(row_5, results)

    def test__select__aggregates(self):
        """"""
        table_name = 'test_queries__select__aggregate'
        # Verify table exists.
        try:
            self.connector.query.execute('CREATE TABLE {0}{1};'.format(table_name, self._columns_clause__aggregates))
        except self.connector.errors.table_already_exists:
            # Table already exists, as we want.
            pass

        # Prepopulate with a few records.
        self.connector.records.insert_many(
            table_name,
            [
                ('test one', 10, False),
                ('test two', 12, False),
                ('test three', 5, False),
                ('test four', 3, False),
                ('test five', 22, False),
            ],
            columns_clause=('test_str, test_int, test_bool'),
        )

        with self.subTest('SELECT with AVG aggregation'):
            # Run test query.
            results = self.connector.records.select(table_name, 'AVG(test_int)')

            # Verify return aggregate result.
            self.assertEqual(len(results), 1)
            self.assertEqual(results[0][0], Decimal('10.4'))

        with self.subTest('SELECT with MAX aggregation'):
            # Run test query.
            results = self.connector.records.select(table_name, 'MAX(test_int)')

            # Verify return aggregate result.
            self.assertEqual(len(results), 1)
            self.assertEqual(results[0][0], 22)

        with self.subTest('SELECT with MIN aggregation'):
            # Run test query.
            results = self.connector.records.select(table_name, 'MIN(test_int)')

            # Verify return aggregate result.
            self.assertEqual(len(results), 1)
            self.assertEqual(results[0][0], 3)

        with self.subTest('SELECT with SUM aggregation'):
            # Run test query.
            results = self.connector.records.select(table_name, 'SUM(test_int)')

            # Verify return aggregate result.
            self.assertEqual(len(results), 1)
            self.assertEqual(results[0][0], 52)

    def test__insert__basic__success(self):
        """
        Test `INSERT` query with basic values.
        """
        table_name = 'test_queries__insert__basic__success'

        # Verify table exists.
        try:
            self.connector.query.execute('CREATE TABLE {0}{1};'.format(table_name, self._columns_clause__basic))
        except self.connector.errors.table_already_exists:
            # Table already exists, as we want.
            pass

        # Verify starting state.
        results = self.connector.query.execute('SELECT * FROM {0};'.format(table_name))
        self.assertEqual(len(results), 0)

        # Run test query.
        row = (1, 'test_name_1', 'test_desc_1')
        self.connector.records.insert(table_name, row)
        results = self.connector.query.execute('SELECT * FROM {0};'.format(table_name))

        # Verify one record returned.
        self.assertEqual(len(results), 1)
        self.assertIn(row, results)

        # Run test query.
        row = (2, 'test_name_2', 'test_desc_2')
        self.connector.records.insert(table_name, row)
        results = self.connector.query.execute('SELECT * FROM {0};'.format(table_name))

        # Verify two records returned.
        self.assertEqual(len(results), 2)
        self.assertIn(row, results)

        # Works for 0, 1, and 2. Assume works for all further n+1 values.

        # Test with columns defined.
        row = (3, 'test_name_3', 'test_desc_3')
        self.connector.records.insert(table_name, row, columns_clause='id, name, description')

    def test__insert__datetime__success(self):
        """
        Test `INSERT` query with datetime values.
        """
        table_name = 'test_queries__insert__datetime__success'

        # Verify table exists.
        try:
            self.connector.query.execute('CREATE TABLE {0} {1};'.format(table_name, self._columns_clause__datetime))
        except self.connector.errors.table_already_exists:
            # Table already exists, as we want.
            pass

        # Verify starting state.
        results = self.connector.query.execute('SELECT * FROM {0};'.format(table_name))
        self.assertEqual(len(results), 0)

        # Generate datetime objects.
        test_datetime__2020 = datetime.datetime(
            year=2020,
            month=6,
            day=15,
            hour=7,
            minute=12,
            second=52,
            microsecond=29,
        )
        test_date__2020 = test_datetime__2020.date()
        test_datetime_str__2020 = test_datetime__2020.strftime('%Y-%m-%d %H:%M:%S')
        test_date_str__2020 = test_date__2020.strftime('%Y-%m-%d')

        # Run test query, using string values.
        row_1 = (1, test_datetime_str__2020, test_date_str__2020)
        self.connector.records.insert(table_name, row_1)
        results = self.connector.query.execute('SELECT * FROM {0};'.format(table_name))

        # Verify record returned.
        self.assertEqual(len(results), 1)
        self.assertIn((1, test_datetime__2020.replace(microsecond=0), test_date__2020), results)

        # Generate new datetime objects.
        test_datetime__2021 = datetime.datetime(
            year=2021,
            month=5,
            day=14,
            hour=6,
            minute=13,
            second=51,
            microsecond=29,
        )
        test_date__2021 = test_datetime__2021.date()

        # Run test query, using literal date objects.
        row_2 = (2, test_datetime__2021, test_date__2021)
        self.connector.records.insert(table_name, row_2)
        results = self.connector.query.execute('SELECT * FROM {0};'.format(table_name))

        # Verify two records returned.
        self.assertEqual(len(results), 2)
        self.assertIn((1, test_datetime__2020.replace(microsecond=0), test_date__2020), results)
        self.assertIn((2, test_datetime__2021.replace(microsecond=0), test_date__2021), results)

    def test__insert_many__success(self):
        """
        Test execute_many `INSERT` query.
        """
        table_name = 'test_queries__insert_many__success'

        # Verify table exists.
        try:
            self.connector.query.execute('CREATE TABLE {0}{1};'.format(table_name, self._columns_clause__basic))
        except self.connector.errors.table_already_exists:
            # Table already exists, as we want.
            pass

        # Verify starting state.
        results = self.connector.query.execute('SELECT * FROM {0};'.format(table_name))
        self.assertEqual(len(results), 0)

        # Generate row values.
        row_1 = (1, 'test_name_1', 'test_desc_1')
        row_2 = (2, 'test_name_2', 'test_desc_2')
        row_3 = (3, 'test_name_3', 'test_desc_3')
        row_4 = (4, 'test_name_4', 'test_desc_4')
        row_5 = (5, 'test_name_5', 'test_desc_5')
        row_6 = (6, 'test_name_6', 'test_desc_6')
        row_7 = (7, 'test_name_7', 'test_desc_7')
        row_8 = (8, 'test_name_8', 'test_desc_8')
        row_9 = (9, 'test_name_9', 'test_desc_9')
        row_10 = (10, 'test_name_10', 'test_desc_10')

        with self.subTest('With one insert'):
            # Run test query.
            rows = [
                row_1,
            ]
            self.connector.records.insert_many(table_name, rows)

            # Verify one record returned.
            results = self.connector.query.execute('SELECT * FROM {0};'.format(table_name))
            self.assertEqual(len(results), 1)
            self.assertIn(row_1, results)

        # Reset table.
        self.connector.tables.drop(table_name)
        self.connector.tables.create(table_name, self._columns_clause__basic)

        with self.subTest('With two inserts'):
            # Run test query.
            rows = [
                row_1,
                row_2,
            ]
            self.connector.records.insert_many(table_name, rows)

            # Verify one record returned.
            results = self.connector.query.execute('SELECT * FROM {0};'.format(table_name))
            self.assertEqual(len(results), 2)
            self.assertIn(row_1, results)
            self.assertIn(row_2, results)

        # Reset table.
        self.connector.tables.drop(table_name)
        self.connector.tables.create(table_name, self._columns_clause__basic)

        with self.subTest('With five inserts'):
            # Run test query.
            rows = [
                row_1,
                row_2,
                row_3,
                row_4,
                row_5,
            ]
            self.connector.records.insert_many(table_name, rows)

            # Verify five records returned.
            results = self.connector.query.execute('SELECT * FROM {0};'.format(table_name))
            self.assertEqual(len(results), 5)
            self.assertIn(row_1, results)
            self.assertIn(row_2, results)
            self.assertIn(row_3, results)
            self.assertIn(row_4, results)
            self.assertIn(row_5, results)

        # Reset table.
        self.connector.tables.drop(table_name)
        self.connector.tables.create(table_name, self._columns_clause__basic)

        with self.subTest('With ten inserts'):
            # Run test query.
            rows = [
                row_1,
                row_2,
                row_3,
                row_4,
                row_5,
                row_6,
                row_7,
                row_8,
                row_9,
                row_10,
            ]
            self.connector.records.insert_many(table_name, rows)

            # Verify ten records returned.
            results = self.connector.query.execute('SELECT * FROM {0};'.format(table_name))
            self.assertEqual(len(results), 10)
            self.assertIn(row_1, results)
            self.assertIn(row_2, results)
            self.assertIn(row_3, results)
            self.assertIn(row_4, results)
            self.assertIn(row_5, results)
            self.assertIn(row_6, results)
            self.assertIn(row_7, results)
            self.assertIn(row_8, results)
            self.assertIn(row_9, results)
            self.assertIn(row_10, results)

    def test__update__basic__success(self):
        """
        Test `UPDATE` query with basic values.
        """
        table_name = 'test_queries__update__basic__success'

        # Verify table exists.
        try:
            self.connector.query.execute('CREATE TABLE {0}{1};'.format(table_name, self._columns_clause__basic))
        except self.connector.errors.table_already_exists:
            # Table already exists, as we want.
            pass

        # Initialize state.
        results = self.connector.query.execute('SELECT * FROM {0};'.format(table_name))
        self.assertEqual(len(results), 0)
        row_1 = (1, 'test_name_1', 'test_desc_1')
        self.connector.query.execute('INSERT INTO {0} VALUES {1};'.format(table_name, row_1))
        row_2 = (2, 'test_name_2', 'test_desc_2')
        self.connector.query.execute('INSERT INTO {0} VALUES {1};'.format(table_name, row_2))
        row_3 = (3, 'test_name_3', 'test_desc_3')
        self.connector.query.execute('INSERT INTO {0} VALUES {1};'.format(table_name, row_3))
        results = self.connector.query.execute('SELECT * FROM {0};'.format(table_name))
        self.assertEqual(len(results), 3)
        self.assertIn(row_1, results)
        self.assertIn(row_2, results)
        self.assertIn(row_3, results)

        with self.subTest('With WHERE clause'):
            # Update row 2 and verify change.
            self.connector.records.update(
                table_name,
                'name = {0}updated name{0}'.format(self.connector.validate._quote_str_literal_format),
                'id = 2',
            )
            results = self.connector.query.execute('SELECT * FROM {0};'.format(table_name))
            old_row_2 = row_2
            row_2 = (2, 'updated name', 'test_desc_2')
            self.assertEqual(len(results), 3)
            self.assertIn(row_1, results)
            self.assertIn(row_2, results)
            self.assertIn(row_3, results)
            self.assertNotIn(old_row_2, results)

            # Update row 3 and verify change.
            self.connector.records.update(
                table_name,
                'description = {0}testing aaa{0}'.format(self.connector.validate._quote_str_literal_format),
                'description = {0}test_desc_3{0}'.format(self.connector.validate._quote_str_literal_format),
            )
            results = self.connector.query.execute('SELECT * FROM {0};'.format(table_name))
            old_row_3 = row_3
            row_3 = (3, 'test_name_3', 'testing aaa')
            self.assertEqual(len(results), 3)
            self.assertIn(row_1, results)
            self.assertIn(row_2, results)
            self.assertIn(row_3, results)
            self.assertNotIn(old_row_2, results)
            self.assertNotIn(old_row_3, results)

            # Update row 1 and verify change.
            self.connector.records.update(table_name, 'id = 4', 'id = 1')
            results = self.connector.query.execute('SELECT * FROM {0};'.format(table_name))
            old_row_1 = row_1
            row_1 = (4, 'test_name_1', 'test_desc_1')
            self.assertEqual(len(results), 3)
            self.assertIn(row_1, results)
            self.assertIn(row_2, results)
            self.assertIn(row_3, results)
            self.assertNotIn(old_row_1, results)
            self.assertNotIn(old_row_2, results)
            self.assertNotIn(old_row_3, results)

        with self.subTest('Without WHERE clause'):
            # Update all rows.
            # Note, to help with database integrity (and prevent accidentally updating all rows via accidental clause
            # omission), we still need to provide the where clause. It's a required arg.
            # But providing a blank clause means we're intentionally setting it to empty, and thus is allowed.
            self.connector.records.update(
                table_name,
                'name = {0}test name{0}'.format(self.connector.validate._quote_str_literal_format),
                '',
            )

            # Verify all rows updated.
            results = self.connector.query.execute('SELECT * FROM {0};'.format(table_name))
            old_row_1 = row_1
            old_row_2 = row_2
            old_row_3 = row_3
            row_1 = (4, 'test name', 'test_desc_1')
            row_2 = (2, 'test name', 'test_desc_2')
            row_3 = (3, 'test name', 'testing aaa')
            self.assertEqual(len(results), 3)
            self.assertIn(row_1, results)
            self.assertIn(row_2, results)
            self.assertIn(row_3, results)
            self.assertNotIn(old_row_1, results)
            self.assertNotIn(old_row_2, results)
            self.assertNotIn(old_row_3, results)

    def test__update__datetime__success(self):
        """
        Test `UPDATE` query with datetime values.
        """
        table_name = 'test_queries__update__datetime__success'

        # Verify table exists.
        try:
            self.connector.query.execute('CREATE TABLE {0}{1};'.format(table_name, self._columns_clause__datetime))
        except self.connector.errors.table_already_exists:
            # Table already exists, as we want.
            pass

        # Generate datetime objects.
        test_datetime__2020 = datetime.datetime(
            year=2020,
            month=6,
            day=15,
            hour=7,
            minute=12,
            second=52,
            microsecond=29,
        )
        test_date__2020 = test_datetime__2020.date()
        test_datetime__2021 = datetime.datetime(
            year=2021,
            month=7,
            day=16,
            hour=8,
            minute=13,
            second=53,
            microsecond=29,
        )
        test_date__2021 = test_datetime__2021.date()
        test_datetime__2022 = datetime.datetime(
            year=2022,
            month=8,
            day=17,
            hour=9,
            minute=14,
            second=54,
            microsecond=29,
        )
        test_date__2022 = test_datetime__2022.date()

        # Initialize state.
        results = self.connector.query.execute('SELECT * FROM {0};'.format(table_name))
        self.assertEqual(len(results), 0)
        row_1 = (1, test_datetime__2020, test_date__2020)
        self.connector.records.insert(table_name, row_1)
        row_1 = (1, test_datetime__2020.replace(microsecond=0), test_date__2020)
        row_2 = (2, test_datetime__2021, test_date__2021)
        self.connector.records.insert(table_name, row_2)
        row_2 = (2, test_datetime__2021.replace(microsecond=0), test_date__2021)
        row_3 = (3, test_datetime__2022, test_date__2022)
        self.connector.records.insert(table_name, row_3)
        row_3 = (3, test_datetime__2022.replace(microsecond=0), test_date__2022)
        results = self.connector.query.execute('SELECT * FROM {0};'.format(table_name))
        self.assertEqual(len(results), 3)
        self.assertIn(row_1, results)
        self.assertIn(row_2, results)
        self.assertIn(row_3, results)

        with self.subTest('With WHERE clause'):
            # Update datetime values.
            updated_test_datetime__2021 = test_datetime__2021 + datetime.timedelta(days=5)
            updated_test_date__2021 = updated_test_datetime__2021.date()
            updated_test_datetime_str__2021 = updated_test_datetime__2021.strftime('%Y-%m-%d %H:%M:%S')
            updated_test_date_str__2021 = updated_test_date__2021.strftime('%Y-%m-%d')

            # Update row 2 and verify change. Use datetime str.
            self.connector.records.update(
                table_name,
                (
                    'test_datetime = {1}{0}{1}, '.format(
                        updated_test_datetime_str__2021,
                        self.connector.validate._quote_str_literal_format,
                    )
                    + 'test_date = {1}{0}{1}'.format(
                        updated_test_date_str__2021,
                        self.connector.validate._quote_str_literal_format,
                    )
                ),
                'id = 2',
            )
            results = self.connector.query.execute('SELECT * FROM {0};'.format(table_name))

            # Sanitize by removing microsecond. Makes it easier to test, while still getting enough accuracy.
            sanitized_results = ()
            for row_index in range(len(results)):
                sanitized_row = ()
                for col_index in range(len(results[row_index])):
                    try:
                        sanitized_row += (results[row_index][col_index].replace(microsecond=0),)
                    except:
                        sanitized_row += (results[row_index][col_index],)
                sanitized_results += (sanitized_row,)
            results = sanitized_results

            row_2 = (2, updated_test_datetime__2021.replace(microsecond=0), updated_test_date__2021)
            old_row_2 = (2, test_datetime__2021.replace(microsecond=0), test_date__2021)
            self.assertEqual(len(results), 3)
            self.assertIn(row_1, results)
            self.assertIn(row_2, results)
            self.assertIn(row_3, results)
            self.assertNotIn(old_row_2, results)

            # Update datetime values.
            updated_test_datetime__2022 = test_datetime__2022 - datetime.timedelta(days=5)
            updated_test_date__2022 = updated_test_datetime__2022.date()

            # Update row 3 and verify change. Use datetime objects.
            # TODO: This isn't very useful when placed directly after above assertions.
            #   Is basically just checking for str format again. Rework after where clause is handled better.
            self.connector.records.update(
                table_name,
                (
                    'test_datetime = {1}{0}{1}, '.format(
                        updated_test_datetime__2022,
                        self.connector.validate._quote_str_literal_format,
                    )
                    + 'test_date = {1}{0}{1}'.format(
                        updated_test_date__2022,
                        self.connector.validate._quote_str_literal_format,
                    )
                ),
                'id = 3',
            )
            results = self.connector.query.execute('SELECT * FROM {0};'.format(table_name))

            # Sanitize by removing microsecond. Makes it easier to test, while still getting enough accuracy.
            sanitized_results = ()
            for row_index in range(len(results)):
                sanitized_row = ()
                for col_index in range(len(results[row_index])):
                    try:
                        sanitized_row += (results[row_index][col_index].replace(microsecond=0),)
                    except:
                        sanitized_row += (results[row_index][col_index],)
                sanitized_results += (sanitized_row,)
            results = sanitized_results

            row_3 = (3, updated_test_datetime__2022.replace(microsecond=0), updated_test_date__2022)
            old_row_3 = (3, test_datetime__2022.replace(microsecond=0), test_date__2022)
            self.assertEqual(len(results), 3)
            self.assertIn(row_1, results)
            self.assertIn(row_2, results)
            self.assertIn(row_3, results)
            self.assertNotIn(old_row_2, results)
            self.assertNotIn(old_row_3, results)

    def test__update_many__basic__success(self):
        """
        Test execute_many `UPDATE` query with basic values.
        """
        table_name = 'test_queries__update_many__basic__success'

        # Verify table exists.
        try:
            self.connector.query.execute('CREATE TABLE {0}{1};'.format(table_name, self._columns_clause__basic))
        except self.connector.errors.table_already_exists:
            # Table already exists, as we want.
            pass

        # Verify starting state.
        results = self.connector.query.execute('SELECT * FROM {0};'.format(table_name))
        self.assertEqual(len(results), 0)

        # Generate row values.
        row_1 = (1, 'test_name_1', 'test_desc_1')
        row_2 = (2, 'test_name_2', 'test_desc_2')
        row_3 = (3, 'test_name_3', 'test_desc_3')
        row_4 = (4, 'test_name_4', 'test_desc_4')
        row_5 = (5, 'test_name_5', 'test_desc_5')
        row_6 = (6, 'test_name_6', 'test_desc_6')
        row_7 = (7, 'test_name_7', 'test_desc_7')
        row_8 = (8, 'test_name_8', 'test_desc_8')
        row_9 = (9, 'test_name_9', 'test_desc_9')
        row_10 = (10, 'test_name_10', 'test_desc_10')

        # Generate initial rows.
        rows = [
            row_1,
            row_2,
            row_3,
            row_4,
            row_5,
            row_6,
            row_7,
            row_8,
            row_9,
            row_10,
        ]
        self.connector.records.insert_many(table_name, rows)

        # Verify expected state.
        results = self.connector.query.execute('SELECT * FROM {0};'.format(table_name))
        self.assertEqual(len(results), 10)
        self.assertIn(row_1, results)
        self.assertIn(row_2, results)
        self.assertIn(row_3, results)
        self.assertIn(row_4, results)
        self.assertIn(row_5, results)
        self.assertIn(row_6, results)
        self.assertIn(row_7, results)
        self.assertIn(row_8, results)
        self.assertIn(row_9, results)
        self.assertIn(row_10, results)

        with self.subTest('With one update'):
            # Run test query.
            updated_row_1 = (1, 'test_name_1_updated', 'test_desc_1')
            columns_clause = ['id', 'name', 'description']
            values_clause = [
                updated_row_1,
            ]
            where_columns_clause = ['id']
            self.connector.records.update_many(table_name, columns_clause, values_clause, where_columns_clause)

            # Verify one record returned.
            results = self.connector.query.execute('SELECT * FROM {0};'.format(table_name))
            self.assertEqual(len(results), 10)
            self.assertIn(updated_row_1, results)
            self.assertIn(row_2, results)
            self.assertIn(row_3, results)
            self.assertIn(row_4, results)
            self.assertIn(row_5, results)
            self.assertIn(row_6, results)
            self.assertIn(row_7, results)
            self.assertIn(row_8, results)
            self.assertIn(row_9, results)
            self.assertIn(row_10, results)
            self.assertNotIn(row_1, results)

            # Update row variables.
            row_1 = updated_row_1

        with self.subTest('With two updates'):
            # Run test query. Update by PK.
            updated_row_2 = (2, 'aaa', 'test_desc_2')
            updated_row_3 = (3, 'bbb', 'test_desc_3')
            columns_clause = ['id', 'name', 'description']
            values_clause = [
                updated_row_2,
                updated_row_3,
            ]
            where_columns_clause = ['id']
            self.connector.records.update_many(table_name, columns_clause, values_clause, where_columns_clause)

            # Verify one record returned.
            results = self.connector.query.execute('SELECT * FROM {0};'.format(table_name))
            self.assertEqual(len(results), 10)
            self.assertIn(row_1, results)
            self.assertIn(updated_row_2, results)
            self.assertIn(updated_row_3, results)
            self.assertIn(row_4, results)
            self.assertIn(row_5, results)
            self.assertIn(row_6, results)
            self.assertIn(row_7, results)
            self.assertIn(row_8, results)
            self.assertIn(row_9, results)
            self.assertIn(row_10, results)
            self.assertNotIn(row_2, results)
            self.assertNotIn(row_3, results)

            # Update row variables.
            row_2 = updated_row_2
            row_3 = updated_row_3

        with self.subTest('With five updates and alternate where column'):
            # Run test query. Update by non-PK.
            updated_row_4 = (4, 'test_name_4', 'four')
            updated_row_5 = (5, 'test_name_5', 'five')
            updated_row_6 = (6, 'test_name_6', 'six')
            updated_row_7 = (7, 'test_name_7', 'seven')
            updated_row_8 = (8, 'test_name_8', 'eight')
            columns_clause = ['id', 'name', 'description']
            values_clause = [
                updated_row_4,
                updated_row_5,
                updated_row_6,
                updated_row_7,
                updated_row_8,
            ]
            where_columns_clause = ['name']
            self.connector.records.update_many(table_name, columns_clause, values_clause, where_columns_clause)

            # Verify five records returned.
            results = self.connector.query.execute('SELECT * FROM {0};'.format(table_name))
            self.assertEqual(len(results), 10)
            self.assertIn(row_1, results)
            self.assertIn(row_2, results)
            self.assertIn(row_3, results)
            self.assertIn(updated_row_4, results)
            self.assertIn(updated_row_5, results)
            self.assertIn(updated_row_6, results)
            self.assertIn(updated_row_7, results)
            self.assertIn(updated_row_8, results)
            self.assertIn(row_9, results)
            self.assertIn(row_10, results)
            self.assertNotIn(row_4, results)
            self.assertNotIn(row_5, results)
            self.assertNotIn(row_6, results)
            self.assertNotIn(row_7, results)
            self.assertNotIn(row_8, results)

            # Update row variables.
            row_4 = updated_row_4
            row_5 = updated_row_5
            row_6 = updated_row_6
            row_7 = updated_row_7
            row_8 = updated_row_8

        with self.subTest('With ten updates'):
            # Run test query.
            updated_row_1 = (1, '"110"', '"10010"')
            updated_row_2 = (2, '"109"', '"10009"')
            updated_row_3 = (3, '"108"', '"10008"')
            updated_row_4 = (4, '"107"', '"10007"')
            updated_row_5 = (5, '"106"', '"10006"')
            updated_row_6 = (6, '"105"', '"10005"')
            updated_row_7 = (7, '"104"', '"10004"')
            updated_row_8 = (8, '"103"', '"10003"')
            updated_row_9 = (9, '"102"', '"10002"')
            updated_row_10 = (10, '"101"', '"10001"')
            columns_clause = 'id, name, description'
            values_clause = [
                updated_row_1,
                updated_row_2,
                updated_row_3,
                updated_row_4,
                updated_row_5,
                updated_row_6,
                updated_row_7,
                updated_row_8,
                updated_row_9,
                updated_row_10,
            ]
            where_columns_clause = 'id'
            self.connector.records.update_many(table_name, columns_clause, values_clause, where_columns_clause)

            # Verify ten records returned.
            results = self.connector.query.execute('SELECT * FROM {0};'.format(table_name))
            self.assertEqual(len(results), 10)
            self.assertIn(updated_row_1, results)
            self.assertIn(updated_row_2, results)
            self.assertIn(updated_row_3, results)
            self.assertIn(updated_row_4, results)
            self.assertIn(updated_row_5, results)
            self.assertIn(updated_row_6, results)
            self.assertIn(updated_row_7, results)
            self.assertIn(updated_row_8, results)
            self.assertIn(updated_row_9, results)
            self.assertIn(updated_row_10, results)
            self.assertNotIn(row_1, results)
            self.assertNotIn(row_2, results)
            self.assertNotIn(row_3, results)
            self.assertNotIn(row_4, results)
            self.assertNotIn(row_5, results)
            self.assertNotIn(row_6, results)
            self.assertNotIn(row_7, results)
            self.assertNotIn(row_8, results)
            self.assertNotIn(row_9, results)
            self.assertNotIn(row_10, results)

            # Update row variables.
            row_1 = updated_row_1
            row_2 = updated_row_2
            row_3 = updated_row_3
            row_4 = updated_row_4
            row_5 = updated_row_5
            row_6 = updated_row_6
            row_7 = updated_row_7
            row_8 = updated_row_8
            row_9 = updated_row_9
            row_10 = updated_row_10

        with self.subTest('With columns in alternate order'):
            # Run test query.
            updated_row_3 = (3, 'name as first', 'desc as second')
            columns_clause = ['name', 'description', 'id']
            values_clause = [
                ('name as first', 'desc as second', 3)
            ]
            where_columns_clause = ['id']
            self.connector.records.update_many(table_name, columns_clause, values_clause, where_columns_clause)

            # Verify one record returned.
            results = self.connector.query.execute('SELECT * FROM {0};'.format(table_name))
            self.assertEqual(len(results), 10)
            self.assertIn(row_1, results)
            self.assertIn(row_2, results)
            self.assertIn(updated_row_3, results)
            self.assertIn(row_4, results)
            self.assertIn(row_5, results)
            self.assertIn(row_6, results)
            self.assertIn(row_7, results)
            self.assertIn(row_8, results)
            self.assertIn(row_9, results)
            self.assertIn(row_10, results)
            self.assertNotIn(row_3, results)

            # Update row variables.
            row_3 = updated_row_3

        with self.subTest('With skipping unused columns'):
            # Run test query.
            updated_row_5 = (5, row_5[1], 'this is')
            updated_row_6 = (6, row_6[1], 'a')
            updated_row_7 = (7, row_7[1], 'test')
            columns_clause = ['id', 'description']
            values_clause = [
                (updated_row_5[0], updated_row_5[2]),
                (updated_row_6[0], updated_row_6[2]),
                (updated_row_7[0], updated_row_7[2]),
            ]
            where_columns_clause = ['id']
            self.connector.records.update_many(table_name, columns_clause, values_clause, where_columns_clause)

            # Verify one record returned.
            results = self.connector.query.execute('SELECT * FROM {0};'.format(table_name))
            self.assertEqual(len(results), 10)
            self.assertIn(row_1, results)
            self.assertIn(row_2, results)
            self.assertIn(row_3, results)
            self.assertIn(row_4, results)
            self.assertIn(updated_row_5, results)
            self.assertIn(updated_row_6, results)
            self.assertIn(updated_row_7, results)
            self.assertIn(row_8, results)
            self.assertIn(row_9, results)
            self.assertIn(row_10, results)
            self.assertNotIn(row_5, results)
            self.assertNotIn(row_6, results)
            self.assertNotIn(row_7, results)

            # Update row variables.
            row_5 = updated_row_5
            row_6 = updated_row_6
            row_7 = updated_row_7

        with self.subTest('With multiple values in WHERE clause'):
            # Run test query.
            updated_row_8 = (row_8[0], row_8[1], 'Some Descriptor Here for 8')
            columns_clause = ['id', 'name', 'description']
            values_clause = [
                updated_row_8,
            ]
            where_columns_clause = ['id', 'name']
            self.connector.records.update_many(table_name, columns_clause, values_clause, where_columns_clause)

            # Verify one record returned.
            results = self.connector.query.execute('SELECT * FROM {0};'.format(table_name))
            self.assertEqual(len(results), 10)
            self.assertIn(row_1, results)
            self.assertIn(row_2, results)
            self.assertIn(row_3, results)
            self.assertIn(row_4, results)
            self.assertIn(row_5, results)
            self.assertIn(row_6, results)
            self.assertIn(row_7, results)
            self.assertIn(updated_row_8, results)
            self.assertIn(row_9, results)
            self.assertIn(row_10, results)
            self.assertNotIn(row_8, results)

            # Update row variables.
            row_8 = updated_row_8

    def test__update_many__datetime__success(self):
        """
        Test execute_many `UPDATE` query with datetime values.
        """
        table_name = 'test_queries__update_many__datetime__success'

        # Verify table exists.
        try:
            self.connector.query.execute('CREATE TABLE {0}{1};'.format(table_name, self._columns_clause__datetime))
        except self.connector.errors.table_already_exists:
            # Table already exists, as we want.
            pass

        # Generate datetime objects.
        test_datetime__2020 = datetime.datetime(
            year=2020,
            month=6,
            day=15,
            hour=7,
            minute=12,
            second=52,
            microsecond=0,
        )
        test_date__2020 = test_datetime__2020.date()
        test_datetime__2021 = datetime.datetime(
            year=2021,
            month=7,
            day=16,
            hour=8,
            minute=13,
            second=53,
            microsecond=0,
        )
        test_date__2021 = test_datetime__2021.date()
        test_datetime__2022 = datetime.datetime(
            year=2022,
            month=8,
            day=17,
            hour=9,
            minute=14,
            second=54,
            microsecond=0,
        )
        test_date__2022 = test_datetime__2022.date()

        # Generate row values.
        row_1 = (1, test_datetime__2020, test_date__2020)
        row_2 = (2, test_datetime__2021, test_date__2021)
        row_3 = (3, test_datetime__2022, test_date__2022)

        # Generate initial rows.
        rows = [
            row_1,
            row_2,
            row_3,
        ]
        self.connector.records.insert_many(table_name, rows)

        # Verify expected state.
        results = self.connector.query.execute('SELECT * FROM {0};'.format(table_name))
        self.assertEqual(len(results), 3)
        self.assertIn(row_1, results)
        self.assertIn(row_2, results)
        self.assertIn(row_3, results)

        columns_clause = ['id', 'test_datetime', 'test_date']
        column_types_clause = ('integer', 'timestamp', 'date')
        where_columns_clause = ['id']

        with self.subTest('With one update'):
            # Run test query.
            updated_row_1 = (1, test_datetime__2020.replace(month=1), test_date__2020.replace(month=2))
            values_clause = [
                updated_row_1,
            ]
            self.connector.records.update_many(
                table_name,
                columns_clause,
                values_clause,
                where_columns_clause,
                column_types_clause=column_types_clause,
            )

            # Verify one record returned.
            results = self.connector.query.execute('SELECT * FROM {0};'.format(table_name))
            self.assertEqual(len(results), 3)
            self.assertIn(updated_row_1, results)
            self.assertIn(row_2, results)
            self.assertIn(row_3, results)
            self.assertNotIn(row_1, results)

            # Update row variables.
            row_1 = updated_row_1

        with self.subTest('With all updated'):
            # Run test query.
            updated_row_1 = (1, test_datetime__2020.replace(day=20), test_date__2020.replace(day=10))
            updated_row_2 = (2, test_datetime__2021.replace(day=20), test_date__2021.replace(day=10))
            updated_row_3 = (3, test_datetime__2022.replace(day=20), test_date__2022.replace(day=10))
            values_clause = [
                updated_row_1,
                updated_row_2,
                updated_row_3,
            ]
            self.connector.records.update_many(
                table_name,
                columns_clause,
                values_clause,
                where_columns_clause,
                column_types_clause=column_types_clause,
            )

            # Verify one record returned.
            results = self.connector.query.execute('SELECT * FROM {0};'.format(table_name))
            self.assertEqual(len(results), 3)
            self.assertIn(updated_row_1, results)
            self.assertIn(updated_row_2, results)
            self.assertIn(updated_row_3, results)
            self.assertNotIn(row_1, results)
            self.assertNotIn(row_2, results)
            self.assertNotIn(row_3, results)

            # Update row variables.
            row_1 = updated_row_1
            row_2 = updated_row_2
            row_3 = updated_row_3

        with self.subTest('With columns in alternate order'):
            # Run test query.
            columns_clause = ['test_date', 'id', 'test_datetime']
            column_types_clause = ['date', 'integer', 'timestamp']
            updated_row_2 = (2, test_datetime__2021.replace(month=3), test_date__2021.replace(month=4))
            updated_row_3 = (3, test_datetime__2022.replace(month=6), test_date__2022.replace(month=5))
            values_clause = [
                (updated_row_2[2], updated_row_2[0], updated_row_2[1]),
                (updated_row_3[2], updated_row_3[0], updated_row_3[1]),
            ]
            self.connector.records.update_many(
                table_name,
                columns_clause,
                values_clause,
                where_columns_clause,
                column_types_clause=column_types_clause,
            )

            # Verify one record returned.
            results = self.connector.query.execute('SELECT * FROM {0};'.format(table_name))
            self.assertEqual(len(results), 3)
            self.assertIn(row_1, results)
            self.assertIn(updated_row_2, results)
            self.assertIn(updated_row_3, results)
            self.assertNotIn(row_2, results)
            self.assertNotIn(row_3, results)

            # Update row variables.
            row_2 = updated_row_2
            row_3 = updated_row_3

        with self.subTest('With skipping unused columns'):
            # Run test query.
            columns_clause = ['id', 'test_datetime']
            column_types_clause = ['integer', 'timestamp']
            updated_row_1 = (1, test_datetime__2020)
            updated_row_2 = (2, test_datetime__2021)
            updated_row_3 = (3, test_datetime__2022)
            values_clause = [
                updated_row_1,
                updated_row_2,
                updated_row_3,
            ]
            self.connector.records.update_many(
                table_name,
                columns_clause,
                values_clause,
                where_columns_clause,
                column_types_clause=column_types_clause,
            )

            # Verify one record returned.
            results = self.connector.query.execute('SELECT * FROM {0};'.format(table_name))
            self.assertEqual(len(results), 3)
            self.assertIn(updated_row_1 + (row_1[2],), results)
            self.assertIn(updated_row_2 + (row_2[2],), results)
            self.assertIn(updated_row_3 + (row_3[2],), results)
            self.assertNotIn(row_1, results)
            self.assertNotIn(row_2, results)
            self.assertNotIn(row_3, results)

            # Update row variables.
            row_1 = updated_row_1
            row_2 = updated_row_2
            row_3 = updated_row_3

    def test__delete__success(self):
        """
        Test `DELETE` query.
        """
        table_name = 'test_queries__delete__success'

        # Verify table exists.
        try:
            self.connector.query.execute('CREATE TABLE {0}{1};'.format(table_name, self._columns_clause__basic))
        except self.connector.errors.table_already_exists:
            # Table already exists, as we want.
            pass

        with self.subTest('With WHERE clause'):
            # Initialize state.
            results = self.connector.query.execute('SELECT * FROM {0};'.format(table_name))
            self.assertEqual(len(results), 0)
            row_1 = (1, 'test_name_1', 'test_desc_1')
            self.connector.query.execute('INSERT INTO {0} VALUES {1};'.format(table_name, row_1))
            row_2 = (2, 'test_name_2', 'test_desc_2')
            self.connector.query.execute('INSERT INTO {0} VALUES {1};'.format(table_name, row_2))
            row_3 = (3, 'test_name_3', 'test_desc_3')
            self.connector.query.execute('INSERT INTO {0} VALUES {1};'.format(table_name, row_3))
            results = self.connector.query.execute('SELECT * FROM {0};'.format(table_name))
            self.assertEqual(len(results), 3)
            self.assertIn(row_1, results)
            self.assertIn(row_2, results)
            self.assertIn(row_3, results)

            # Remove record 2.
            self.connector.records.delete(table_name, 'id = 2')
            results = self.connector.query.execute('SELECT * FROM {0};'.format(table_name))
            self.assertEqual(len(results), 2)
            self.assertIn(row_1, results)
            self.assertNotIn(row_2, results)
            self.assertIn(row_3, results)

            # Remove record 1.
            self.connector.records.delete(table_name, 'id = 1')
            results = self.connector.query.execute('SELECT * FROM {0};'.format(table_name))
            self.assertEqual(len(results), 1)
            self.assertNotIn(row_1, results)
            self.assertNotIn(row_2, results)
            self.assertIn(row_3, results)

            # Remove record 1.
            self.connector.records.delete(table_name, 'id = 3')
            results = self.connector.query.execute('SELECT * FROM {0};'.format(table_name))
            self.assertEqual(len(results), 0)

        with self.subTest('Without WHERE clause'):
            # Update all rows.
            # Note, to help with database integrity (and prevent accidentally deleting all rows via accidental clause
            # omission), we still need to provide the where clause. It's a required arg.
            # However, providing a blank clause means we're intentionally setting it to empty, and thus is allowed.

            # Initialize state.
            results = self.connector.query.execute('SELECT * FROM {0};'.format(table_name))
            self.assertEqual(len(results), 0)
            row_1 = (1, 'test_name_1', 'test_desc_1')
            self.connector.query.execute('INSERT INTO {0} VALUES {1};'.format(table_name, row_1))
            row_2 = (2, 'test_name_2', 'test_desc_2')
            self.connector.query.execute('INSERT INTO {0} VALUES {1};'.format(table_name, row_2))
            row_3 = (3, 'test_name_3', 'test_desc_3')
            self.connector.query.execute('INSERT INTO {0} VALUES {1};'.format(table_name, row_3))
            results = self.connector.query.execute('SELECT * FROM {0};'.format(table_name))
            self.assertEqual(len(results), 3)
            self.assertIn(row_1, results)
            self.assertIn(row_2, results)
            self.assertIn(row_3, results)

            # Remove all records.
            self.connector.records.delete(table_name, '')
            results = self.connector.query.execute('SELECT * FROM {0};'.format(table_name))
            self.assertEqual(len(results), 0)
