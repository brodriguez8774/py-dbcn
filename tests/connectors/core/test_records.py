"""
Initialization of"records" logic of "Core" DB Connector class.

Note that the tests for the "Core" DB Connector class don't do anything in themselves.
They're meant to define a majority of overall database logic, which is then inherited/tweaked by the
various specific database test classes. This ensures that all databases types run similar/equal tests.
"""

# System Imports.

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
        Test `SELECT` query when table does not exist.
        """
        table_name = 'test_queries__select__success'

        # Verify table exists.
        try:
            self.connector.query.execute('CREATE TABLE {0}{1};'.format(table_name, self._columns_query))
        except self.db_error_handler.OperationalError:
            # Table already exists, as we want.
            pass

        with self.subTest('SELECT query when table has no records'):
            # Run test query.
            results = self.connector.tables.show()

            # Verify no records returned.
            self.assertGreaterEqual(len(results), 0)
            self.assertIn(table_name, results)

        with self.subTest('SELECT query when table has records'):
            # Run test query.
            row = (1, 'test_name_1', 'test_desc_1')
            self.connector.query.execute('INSERT INTO {0} VALUES {1};'.format(table_name, row))
            results = self.connector.records.select(table_name)

            # Verify one record returned.
            self.assertEqual(len(results), 1)
            self.assertIn(row, results)

            # Run test query.
            row = (2, 'test_name_2', 'test_desc_2')
            self.connector.query.execute('INSERT INTO {0} VALUES {1};'.format(table_name, row))
            results = self.connector.records.select(table_name)

            # Verify two records returned.
            self.assertEqual(len(results), 2)
            self.assertIn(row, results)

        # Works for 0, 1, and 2. Assume works for all further n+1 values.

        with self.subTest('SELECT query when table column uses "reserved keyword"'):
            # "Group" is considered a MySQL keyword. As long as this doesn't raise an error, it worked.
            self.connector.tables.add_column(table_name, '`group` VARCHAR(100)')
            results = self.connector.records.select(table_name)

            # Verify two records returned, now with an extra "group" field that shows null.
            row = row + (None,)
            self.assertEqual(len(results), 2)
            self.assertIn(row, results)

    def test__insert__success(self):
        """
        Test `INSERT` query when table does not exist.
        """
        table_name = 'test_queries__insert__success'

        # Verify table exists.
        try:
            self.connector.query.execute('CREATE TABLE {0}{1};'.format(table_name, self._columns_query))
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

    def test__update__success(self):
        """
        Test `UPDATE` query when table does not exist.
        """
        table_name = 'test_queries__update__success'

        # Verify table exists.
        try:
            self.connector.query.execute('CREATE TABLE {0}{1};'.format(table_name, self._columns_query))
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
            pass
            # raise NotImplementedError()

    def test__delete__success(self):
        """
        Test `DELETE` query when table does not exist.
        """
        table_name = 'test_queries__delete__success'

        # Verify table exists.
        try:
            self.connector.query.execute('CREATE TABLE {0}{1};'.format(table_name, self._columns_query))
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
