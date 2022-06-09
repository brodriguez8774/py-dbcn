"""
Tests for "tables" logic of "MySQL" DB Connector class.
"""

# System Imports.

# User Imports.
import MySQLdb

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
