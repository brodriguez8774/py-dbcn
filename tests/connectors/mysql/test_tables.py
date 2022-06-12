"""
Tests for "tables" logic of "MySQL" DB Connector class.
"""

# System Imports.
import MySQLdb

# User Imports.
from .test_core import TestMysqlDatabaseParent


class TestMysqlTables(TestMysqlDatabaseParent):
    """
    Tests "MySQL" DB Connector class table logic.
    """
    @classmethod
    def setUpClass(cls):
        # Run parent setup logic.
        super().setUpClass()

        # Initialize database for tests.
        db_name = 'python__db_connector__test_tables'
        cls.connector.database.create(db_name)
        cls.connector.database.use(db_name)

        # Define default table columns.
        cls._columns_query = """(
            id INT NOT NULL AUTO_INCREMENT,
            name VARCHAR(100),
            description VARCHAR(100),
            PRIMARY KEY ( id )
        )"""

    def test__show_tables(self):
        """
        Test logic for `SHOW TABLES;` query
        """
        table_name = 'test_tables__show'

        with self.subTest('SHOW query when table exists'):
            # Verify table exists.
            try:
                self.connector.query.execute('CREATE TABLE {0}{1};'.format(table_name, self._columns_query))
            except MySQLdb.OperationalError:
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
            except MySQLdb.OperationalError:
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
            self.connector.query.execute('DROP TABLE {0};'.format(table_name))
        except MySQLdb.OperationalError:
            # Table does not yet exist, as we want.
            pass

        # Check tables prior to test query. Verify expected table did not return.
        results = self.connector.tables.show()
        self.assertNotIn(table_name, results)

        # Run test query.
        self.connector.tables.create(table_name, self._columns_query)

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
            self.connector.query.execute('CREATE TABLE {0}{1};'.format(table_name, self._columns_query))
        except MySQLdb.OperationalError:
            # Table already exists, as we want.
            pass

        # Check tables prior to test query. Verify expected table returned.
        results = self.connector.tables.show()
        self.assertGreaterEqual(len(results), 1)
        self.assertIn(table_name, results)

        # Run test query.
        with self.assertRaises(ValueError):
            self.connector.tables.create(table_name, self._columns_query)

    def test__modify_table__success(self):
        """
        Test `ALTER TABLE` query.
        """
        table_name = 'test_tables__modify__success'
        col_1_description = ('id', 'int', 'NO', 'PRI', None, 'auto_increment')
        col_2_description = ('name', 'varchar(100)', 'YES', '', None, '')
        col_3_description = ('description', 'varchar(100)', 'YES', '', None, '')

        # Verify table exists.
        try:
            self.connector.query.execute('CREATE TABLE {0}{1};'.format(table_name, self._columns_query))
        except MySQLdb.OperationalError:
            # Table already exists, as we want.
            pass

        # Check tables prior to test query. Verify expected table columns.
        results = self.connector.tables.describe(table_name)
        self.assertEqual(len(results), 3)
        self.assertIn(col_1_description, results)
        self.assertIn(col_2_description, results)
        self.assertIn(col_3_description, results)

        # Test dropping name and desc columns.
        self.connector.tables.modify(table_name, 'DROP', 'name')

        # Check after first drop.
        results = self.connector.tables.describe(table_name)
        self.assertEqual(len(results), 2)
        self.assertIn(col_1_description, results)
        self.assertNotIn(col_2_description, results)
        self.assertIn(col_3_description, results)

        # Drop again, with alternative alias method.
        self.connector.tables.drop_column(table_name, 'description')

        # Check after second drop.
        results = self.connector.tables.describe(table_name)
        self.assertEqual(len(results), 1)
        self.assertIn(col_1_description, results)
        self.assertNotIn(col_2_description, results)
        self.assertNotIn(col_3_description, results)

        # Test adding them back.
        self.connector.tables.modify(table_name, 'ADD', 'description VARCHAR(100)')

        # Check after first add.
        results = self.connector.tables.describe(table_name)
        self.assertEqual(len(results), 2)
        self.assertIn(col_1_description, results)
        self.assertNotIn(col_2_description, results)
        self.assertIn(col_3_description, results)

        # Drop again, with alternative alias method.
        self.connector.tables.add_column(table_name, 'name VARCHAR(100)')

        # Check after second add.
        results = self.connector.tables.describe(table_name)
        self.assertEqual(len(results), 3)
        self.assertIn(col_1_description, results)
        self.assertIn(col_2_description, results)
        self.assertIn(col_3_description, results)

        # Alter columns to be different types.
        self.connector.tables.modify(table_name, 'MODIFY', 'name INT')
        old_col_2_description = col_2_description
        col_2_description = ('name', 'int', 'YES', '', None, '')

        # Check after first modify.
        results = self.connector.tables.describe(table_name)
        self.assertEqual(len(results), 3)
        self.assertIn(col_1_description, results)
        self.assertIn(col_2_description, results)
        self.assertIn(col_3_description, results)
        self.assertNotIn(old_col_2_description, results)

        # Drop again, with alternative alias method.
        self.connector.tables.modify_column(table_name, 'description BOOL')
        old_col_3_description = col_3_description
        col_3_description = ('description', 'tinyint(1)', 'YES', '', None, '')

        # Check after second add.
        results = self.connector.tables.describe(table_name)
        self.assertEqual(len(results), 3)
        self.assertIn(col_1_description, results)
        self.assertIn(col_2_description, results)
        self.assertIn(col_3_description, results)
        self.assertNotIn(old_col_2_description, results)
        self.assertNotIn(old_col_3_description, results)

    def test__delete_table__success(self):
        """
        Test `DROP TABLE` query, when table exists.
        """
        table_name = 'test_tables__delete__success'

        # Verify table exists.
        try:
            self.connector.query.execute('CREATE TABLE {0}{1};'.format(table_name, self._columns_query))
        except MySQLdb.OperationalError:
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
        table_name = 'test_tables__count'

        # Verify table exists.
        try:
            self.connector.query.execute('CREATE TABLE {0}{1};'.format(table_name, self._columns_query))
        except MySQLdb.OperationalError:
            # Table already exists, as we want.
            pass

        # Check tables prior to test query. Verify expected table returned.
        results = self.connector.tables.show()
        self.assertGreaterEqual(len(results), 1)
        self.assertIn(table_name, results)

        # Run test query with empty table.
        results = self.connector.tables.count(table_name)
        self.assertEqual(results, 0)

        # Add one record and run test query again.
        self.connector.query.execute('INSERT INTO {0} VALUES (1, "test_name_1", "test_desc_1");'.format(table_name))
        results = self.connector.tables.count(table_name)
        self.assertEqual(results, 1)

        # # Add second record and run test query again.
        self.connector.query.execute('INSERT INTO {0} VALUES (2, "test_name_2", "test_desc_2");'.format(table_name))
        results = self.connector.tables.count(table_name)
        self.assertEqual(results, 2)

        # Works for 0, 1, and 2. Assume works for all further n+1 values.
