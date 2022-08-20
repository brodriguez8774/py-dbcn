"""
Initialization of"records" logic of "Core" DB Connector class.

Note that the tests for the "Core" DB Connector class don't do anything in themselves.
They're meant to define a majority of overall database logic, which is then inherited/tweaked by the
various specific database test classes. This ensures that all databases types run similar/equal tests.
"""

# System Imports.
import datetime

# User Imports.


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

    def test__select__success(self):
        """
        Test `SELECT` query.
        """
        table_name = 'test_queries__select__success'

        # Verify table exists.
        try:
            self.connector.query.execute('CREATE TABLE {0}{1};'.format(table_name, self._columns_query__basic))
        except self.db_error_handler.OperationalError:
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
            # "Group" is considered a MySQL keyword. As long as this doesn't raise an error, it worked.
            self.connector.tables.add_column(table_name, '`group` VARCHAR(100)')
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
            self.connector.query.execute('CREATE TABLE {0}{1};'.format(table_name, self._columns_query__basic))
        except self.db_error_handler.OperationalError:
            # Table already exists, as we want.
            pass

        with self.subTest('SELECT with WHERE when table has no records'):
            # Run test query.
            results = self.connector.records.select(table_name, where_clause='description = "test aaa"')

            # Verify no records returned.
            self.assertEqual(len(results), 0)

        with self.subTest('SELECT with WHERE when table has one unrelated record'):
            # Insert record.
            row_1 = (1, 'test_name_1', 'test_desc_1')
            self.connector.query.execute('INSERT INTO {0} VALUES {1};'.format(table_name, row_1))

            # Run test query.
            results = self.connector.records.select(table_name, where_clause='description = "test aaa"')

            # Verify no records returned.
            self.assertEqual(len(results), 0)

        with self.subTest('SELECT with WHERE when table has one unrelated record and one related'):
            # Insert record.
            row_2 = (2, 'test_name_2', 'test aaa')
            self.connector.query.execute('INSERT INTO {0} VALUES {1};'.format(table_name, row_2))

            # Run test query.
            results = self.connector.records.select(table_name, where_clause='description = "test aaa"')

            # Verify no records returned.
            self.assertEqual(len(results), 1)
            self.assertIn(row_2, results)
            self.assertNotIn(row_1, results)

        with self.subTest('SELECT with WHERE when table has two unrelated records and one related'):
            # Insert record.
            row_3 = (3, 'test aaa', 'test_desc_3')
            self.connector.query.execute('INSERT INTO {0} VALUES {1};'.format(table_name, row_3))

            # Run test query.
            results = self.connector.records.select(table_name, where_clause='description = "test aaa"')

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
            results = self.connector.records.select(table_name, where_clause='description = "test aaa"')

            # Verify no records returned.
            self.assertEqual(len(results), 2)
            self.assertIn(row_2, results)
            self.assertIn(row_4, results)
            self.assertNotIn(row_1, results)
            self.assertNotIn(row_3, results)

    def test__insert__basic__success(self):
        """
        Test `INSERT` query with basic values.
        """
        table_name = 'test_queries__insert__basic__success'

        # Verify table exists.
        try:
            self.connector.query.execute('CREATE TABLE {0}{1};'.format(table_name, self._columns_query__basic))
        except self.db_error_handler.OperationalError:
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

    def test__insert__datetime__success(self):
        """
        Test `INSERT` query with datetime values.
        """
        table_name = 'test_queries__insert__datetime__success'

        # Verify table exists.
        try:
            self.connector.query.execute('CREATE TABLE {0}{1};'.format(table_name, self._columns_query__datetime))
        except self.db_error_handler.OperationalError:
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

    def test__update__basic__success(self):
        """
        Test `UPDATE` query.
        """
        table_name = 'test_queries__update__basic__success'

        # Verify table exists.
        try:
            self.connector.query.execute('CREATE TABLE {0}{1};'.format(table_name, self._columns_query__basic))
        except self.db_error_handler.OperationalError:
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
            self.connector.records.update(table_name, 'name = "updated name"', 'id = 2')
            results = self.connector.query.execute('SELECT * FROM {0};'.format(table_name))
            old_row_2 = row_2
            row_2 = (2, 'updated name', 'test_desc_2')
            self.assertEqual(len(results), 3)
            self.assertIn(row_1, results)
            self.assertIn(row_2, results)
            self.assertIn(row_3, results)
            self.assertNotIn(old_row_2, results)

            # Update row 3 and verify change.
            self.connector.records.update(table_name, 'description = "testing aaa"', 'description = "test_desc_3"')
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
            self.connector.records.update(table_name, 'name = "test name"', '')

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
        Test `UPDATE` query.
        """
        table_name = 'test_queries__update__datetime__success'

        # Verify table exists.
        try:
            self.connector.query.execute('CREATE TABLE {0}{1};'.format(table_name, self._columns_query__datetime))
        except self.db_error_handler.OperationalError:
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
                    'test_datetime = "{0}", '.format(updated_test_datetime_str__2021) +
                    'test_date = "{0}"'.format(updated_test_date_str__2021)
                ),
                'id = 2',
            )
            results = self.connector.query.execute('SELECT * FROM {0};'.format(table_name))
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
                    'test_datetime = "{0}", '.format(updated_test_datetime__2022) +
                    'test_date = "{0}"'.format(updated_test_date__2022)
                ),
                'id = 3',
            )
            results = self.connector.query.execute('SELECT * FROM {0};'.format(table_name))
            row_3 = (3, updated_test_datetime__2022.replace(microsecond=0), updated_test_date__2022)
            old_row_3 = (3, test_datetime__2022.replace(microsecond=0), test_date__2022)
            self.assertEqual(len(results), 3)
            self.assertIn(row_1, results)
            self.assertIn(row_2, results)
            self.assertIn(row_3, results)
            self.assertNotIn(old_row_2, results)
            self.assertNotIn(old_row_3, results)

    def test__delete__success(self):
        """
        Test `DELETE` query.
        """
        table_name = 'test_queries__delete__success'

        # Verify table exists.
        try:
            self.connector.query.execute('CREATE TABLE {0}{1};'.format(table_name, self._columns_query__basic))
        except self.db_error_handler.OperationalError:
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
