"""
Initialization of "tables" logic of "Core" DB Connector class.

Note that the tests for the "Core" DB Connector class don't do anything in themselves.
They're meant to define a majority of overall database logic, which is then inherited/tweaked by the
various specific database test classes. This ensures that all databases types run similar/equal tests.
"""

# System Imports.

# Internal Imports.


class CoreTablesTestMixin:
    """
    Tests "Core" DB Connector class table logic.
    """
    @classmethod
    def set_up_class(cls):
        """
        Acts as the equivalent of the UnitTesting "setUpClass()" function.

        However, since this is not inheriting from a given TestCase,
        calling the literal function here would override instead.
        """
        cls.test_db_name_start = cls.test_db_name_start.format(cls.db_type)

    def test_error_catch_types(self):
        """Tests to ensure database ERROR types are properly caught.

        For example, MySQL and PostgreSQL interfaces do not catch "Database Does Not Exist" errors the same way.
        These tests make sure this error (and others) are properly caught, regardless of what database is being called.
        """
        # Ensure error types are first defined.
        if not self.connector.errors.table_does_not_exist:
            raise ValueError('Please define error handler for "Table Does Not Exist" error type.')
        if not self.connector.errors.table_already_exists:
            raise ValueError('Please define error handler for "Table Already Exists" error type.')

    def test__create_table___col_str(self):
        """
        Tests that connector object properly creates new tables, via str of column data.
        """
        table_name = 'test_tables__col_str'

        # Check that expected table DOES NOT yet exist in database.
        results = self.connector.tables.show()
        self.assertNotIn(table_name, results)

        # Attempt to generate table.
        self.connector.tables.create(table_name, self._columns_clause__minimal)

        # Check that expected table now exists in database.
        results = self.connector.tables.show()
        self.assertIn(table_name, results)

    # def test__create_table___col_dict(self):
    #     """
    #     Tests that connector object properly creates new tables, via dict of column data.
    #     """
    #     table_name = 'test_tables__col_dict'
    #
    #     # Check that expected table DOES NOT yet exist in database.
    #     results = self.connector.tables.show()
    #     self.assertNotIn(table_name, results)
    #
    #     # Attempt to generate table.
    #     self.connector.tables.create(table_name, 'id INT(11) NOT NULL AUTO_INCREMENT, PRIMARY KEY (id)')
    #
    #     # Check that expected table now exists in database.
    #     results = self.connector.tables.show()
    #     self.assertIn(table_name, results)

    def test__drop_table(self):
        """
        Tests that connector object properly drops tables.
        """
        table_name = 'test_tables__drop'

        # Check that expected table DOES NOT yet exist in database.
        results = self.connector.tables.show()
        self.assertNotIn(table_name, results)

        # Attempt to generate table.
        self.connector.tables.create(table_name, self._columns_clause__minimal)

        # Check that expected table now exists in database.
        results = self.connector.tables.show()
        self.assertIn(table_name, results)

        # Attempt to remove table.
        self.connector.tables.drop(table_name)

        # Check that expected table was removed.
        results = self.connector.tables.show()
        self.assertNotIn(table_name, results)

    def test__show_tables(self):
        """
        Test logic for `SHOW TABLES;` query
        """
        table_name = 'test_tables__show'

        with self.subTest('SHOW query when table exists'):
            # Verify table exists.
            try:
                self.connector.query.execute('CREATE TABLE {0}{1};'.format(table_name, self._columns_clause__basic))
            except self.connector.errors.table_already_exists:
                # Table already exists, as we want.
                pass

            # Run test query.
            results = self.connector.tables.show()

            # Verify expected table returned.
            self.assertGreaterEqual(len(results), 1)
            self.assertIn(table_name, results)

        # Remove table and verify expected results changed.
        with self.subTest('SHOW query when table does not exist'):
            # Verify table does not exist.
            try:
                self.connector.query.execute('DROP TABLE {0};'.format(table_name))
            except self.connector.errors.table_does_not_exist:
                # Table does not yet exist, as we want.
                pass

            # Run test query.
            results = self.connector.tables.show()

            # Verify expected table did not return.
            self.assertNotIn(table_name, results)

    def test__create_table__success(self):
        """
        Test `CREATE TABLE` query when table does not exist.
        """
        table_name = 'test_tables__create__success'

        # Verify table does not exist.
        try:
            self.connector.tables.drop(table_name)
        except ValueError:
            # Table does not yet exist, as we want.
            pass

        # Check tables prior to test query. Verify expected table did not return.
        results = self.connector.tables.show()
        self.assertNotIn(table_name, results)

        # Run test query.
        self.connector.tables.create(table_name, self._columns_clause__basic)

        # Check tables after test query. Verify expected table returned.
        results = self.connector.tables.show()
        self.assertGreaterEqual(len(results), 1)
        self.assertIn(table_name, results)

    def test__create_table__failure(self):
        """
        Test `CREATE TABLE` query when table exists.
        """
        table_name = 'test_tables__create__failure'

        # Verify table exists.
        try:
            self.connector.query.execute('CREATE TABLE {0}{1};'.format(table_name, self._columns_clause__basic))
        except self.connector.errors.table_already_exists:
            # Table already exists, as we want.
            pass

        # Check tables prior to test query. Verify expected table returned.
        results = self.connector.tables.show()
        self.assertGreaterEqual(len(results), 1)
        self.assertIn(table_name, results)

        # Run test query.
        with self.assertRaises(ValueError):
            self.connector.tables.create(table_name, self._columns_clause__basic)

    # def test__modify_table__success(self):
    #     """
    #     Test `ALTER TABLE` query.
    #     """
    #     table_name = 'test_tables__modify__success'
    #     col_1_description = ('id', 'int', 'NO', 'PRI', None, 'auto_increment')
    #     col_2_description = ('name', 'varchar(100)', 'YES', '', None, '')
    #     col_3_description = ('description', 'varchar(100)', 'YES', '', None, '')
    #
    #     # Verify table exists.
    #     try:
    #         self.connector.query.execute('CREATE TABLE {0}{1};'.format(table_name, _columns_clause__basic))
    #     except self.connector.errors.table_already_exists:
    #         # Table already exists, as we want.
    #         pass
    #
    #     # Check tables prior to test query. Verify expected table columns.
    #     results = self.connector.tables.describe(table_name)
    #     self.assertEqual(len(results), 3)
    #     self.assertIn(col_1_description, results)
    #     self.assertIn(col_2_description, results)
    #     self.assertIn(col_3_description, results)
    #
    #     # Test dropping name and desc columns.
    #     self.connector.tables.modify(table_name, 'DROP', 'name')
    #
    #     # Check after first drop.
    #     results = self.connector.tables.describe(table_name)
    #     self.assertEqual(len(results), 2)
    #     self.assertIn(col_1_description, results)
    #     self.assertNotIn(col_2_description, results)
    #     self.assertIn(col_3_description, results)
    #
    #     # Drop again, with alternative alias method.
    #     self.connector.tables.drop_column(table_name, 'description')
    #
    #     # Check after second drop.
    #     results = self.connector.tables.describe(table_name)
    #     self.assertEqual(len(results), 1)
    #     self.assertIn(col_1_description, results)
    #     self.assertNotIn(col_2_description, results)
    #     self.assertNotIn(col_3_description, results)
    #
    #     # Test adding them back.
    #     self.connector.tables.modify(table_name, 'ADD', 'description VARCHAR(100)')
    #
    #     # Check after first add.
    #     results = self.connector.tables.describe(table_name)
    #     self.assertEqual(len(results), 2)
    #     self.assertIn(col_1_description, results)
    #     self.assertNotIn(col_2_description, results)
    #     self.assertIn(col_3_description, results)
    #
    #     # Drop again, with alternative alias method.
    #     self.connector.tables.add_column(table_name, 'name VARCHAR(100)')
    #
    #     # Check after second add.
    #     results = self.connector.tables.describe(table_name)
    #     self.assertEqual(len(results), 3)
    #     self.assertIn(col_1_description, results)
    #     self.assertIn(col_2_description, results)
    #     self.assertIn(col_3_description, results)
    #
    #     # Alter columns to be different types.
    #     self.connector.tables.modify(table_name, 'MODIFY', 'name INT')
    #     old_col_2_description = col_2_description
    #     col_2_description = ('name', 'int', 'YES', '', None, '')
    #
    #     # Check after first modify.
    #     results = self.connector.tables.describe(table_name)
    #     self.assertEqual(len(results), 3)
    #     self.assertIn(col_1_description, results)
    #     self.assertIn(col_2_description, results)
    #     self.assertIn(col_3_description, results)
    #     self.assertNotIn(old_col_2_description, results)
    #
    #     # Drop again, with alternative alias method.
    #     self.connector.tables.modify_column(table_name, 'description BOOL')
    #     old_col_3_description = col_3_description
    #     col_3_description = ('description', 'tinyint(1)', 'YES', '', None, '')
    #
    #     # Check after second add.
    #     results = self.connector.tables.describe(table_name)
    #     self.assertEqual(len(results), 3)
    #     self.assertIn(col_1_description, results)
    #     self.assertIn(col_2_description, results)
    #     self.assertIn(col_3_description, results)
    #     self.assertNotIn(old_col_2_description, results)
    #     self.assertNotIn(old_col_3_description, results)

    def test__delete_table__success(self):
        """
        Test `DROP TABLE` query, when table exists.
        """
        table_name = 'test_tables__delete__success'

        # Verify table exists.
        try:
            self.connector.query.execute('CREATE TABLE {0}{1};'.format(table_name, self._columns_clause__basic))
        except self.connector.errors.table_already_exists:
            # Table already exists, as we want.
            pass

        # Check tables prior to test query. Verify expected table returned.
        results = self.connector.tables.show()
        self.assertGreaterEqual(len(results), 1)
        self.assertIn(table_name, results)

    def test__count_table(self):
        """
        Test `COUNT TABLE` query.
        """
        if not self.connector.validate._quote_str_literal_format:
            raise ValueError('String literal quote format is not defined.')

        table_name = 'test_tables__count'

        # Verify table exists.
        # try:
        self.connector.query.execute('CREATE TABLE {0}{1};'.format(table_name, self._columns_clause__basic))

        # Check tables prior to test query. Verify expected table returned.
        results = self.connector.tables.show()
        self.assertGreaterEqual(len(results), 1)
        self.assertIn(table_name, results)

        # Run test query with empty table.
        results = self.connector.tables.count(table_name)
        self.assertEqual(results, 0)

        # Add one record and run test query again.
        self.connector.query.execute('INSERT INTO {0} VALUES (1, {1}test_name_1{1}, {1}test_desc_1{1});'.format(
            table_name,
            self.connector.validate._quote_str_literal_format,
        ))
        results = self.connector.tables.count(table_name)
        self.assertEqual(results, 1)

        # # Add second record and run test query again.
        self.connector.query.execute('INSERT INTO {0} VALUES (2, {1}test_name_2{1}, {1}test_desc_2{1});'.format(
            table_name,
            self.connector.validate._quote_str_literal_format,
        ))
        results = self.connector.tables.count(table_name)
        self.assertEqual(results, 2)

        # Works for 0, 1, and 2. Assume works for all further n+1 values.

