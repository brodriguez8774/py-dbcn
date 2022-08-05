"""
Tests for "database" logic of "MySQL" DB Connector class.
"""

# System Imports.
import MySQLdb

# User Imports.
from .test_core import TestMysqlDatabaseParent
from tests.connectors.core.test_database import CoreDatabaseTestMixin


class TestMysqlDatabase(TestMysqlDatabaseParent, CoreDatabaseTestMixin):
    """
    Tests "MySQL" DB Connector class database logic.
    """
    @classmethod
    def setUpClass(cls):
        # Run parent setup logic.
        super().setUpClass()

        # Also call CoreTestMixin setup logic.
        cls.set_up_class()

        # Define database name to use in tests.
        cls.test_db_name = '{0}test_database'.format(cls.test_db_name_start)

        # Initialize database for tests.
        cls.connector.database.create(cls.test_db_name)
        cls.connector.database.use(cls.test_db_name)

        # Check that database has no tables.
        results = cls.connector.tables.show()
        if len(results) > 0:
            for result in results:
                cls.connector.tables.drop(result)

    def test__select(self):
        """
        Test logic for `SELECT;` query.
        """
        with self.subTest('With default database selected'):
            # Varify default database name is returned.
            result = self.connector.database.select()
            self.assertEqual(result, self.test_db_name)

            # Verify alias func returns same result.
            result = self.connector.database.current()
            self.assertEqual(result, self.test_db_name)

        with self.subTest('With select_1 database selected'):
            db_name = '{0}__select_1'.format(self.test_db_name)

            # Verify database exists.
            try:
                self.connector.query.execute('CREATE DATABASE {0};'.format(db_name))
            except MySQLdb.ProgrammingError:
                # Database already exists, as we want.
                pass

            # Switch databases and verify select changed.
            self.connector.database.use(db_name)
            result = self.connector.database.select()
            self.assertEqual(result, db_name)

            # Verify alias func returns same result.
            result = self.connector.database.current()
            self.assertEqual(result, db_name)

        with self.subTest('With select_2 database selected'):
            db_name = '{0}__select_2'.format(self.test_db_name)

            # Verify database exists.
            try:
                self.connector.query.execute('CREATE DATABASE {0};'.format(db_name))
            except MySQLdb.ProgrammingError:
                # Database already exists, as we want.
                pass

            # Switch databases and verify select changed.
            self.connector.database.use(db_name)
            result = self.connector.database.select()
            self.assertEqual(result, db_name)

            # Verify alias func returns same result.
            result = self.connector.database.current()
            self.assertEqual(result, db_name)

    def test__show_database(self):
        """
        Test logic for `SHOW DATABASES;` query.
        """
        db_name = '{0}__show'.format(self.test_db_name)

        with self.subTest('SHOW query when database exists'):
            # Verify database exists.
            try:
                self.connector.query.execute('CREATE DATABASE {0};'.format(db_name))
            except MySQLdb.ProgrammingError:
                # Database already exists, as we want.
                pass

            # Run test query.
            results = self.connector.database.show()

            # Verify at least one database returned.
            self.assertGreaterEqual(len(results), 1)

            # Verify expected database returned.
            self.assertIn(db_name, results)

        # Remove database and verify expected results changed.
        with self.subTest('SHOW query when database does not exist'):
            # Verify database does not exist.
            try:
                self.connector.query.execute('DROP DATABASE {0};'.format(db_name))
            except MySQLdb.OperationalError:
                # Database does not yet exist, as we want.
                pass

            # Run test query.
            results = self.connector.database.show()

            # Verify expected database did not return.
            self.assertNotIn(db_name, results)

    def test__create_database__success(self):
        """
        Test `CREATE DATABASE` query, when database does not exist.
        """
        db_name = '{0}__create__success'.format(self.test_db_name)

        # Verify database does not yet exist.
        try:
            self.connector.query.execute('DROP DATABASE {0};'.format(db_name))
        except MySQLdb.OperationalError:
            # Database does not yet exist, as we want.
            pass

        # Check databases prior to test query. Verify expected database did not return.
        results = self.connector.database.show()
        self.assertNotIn(db_name, results)

        # Run test query.
        self.connector.database.create(db_name)

        # Check databases after test query. Verify expected database returned.
        results = self.connector.database.show()
        self.assertGreaterEqual(len(results), 1)
        self.assertIn(db_name, results)

    def test__create_database__failure(self):
        """
        Test `CREATE DATABASE` query, when database exists.
        """
        db_name = '{0}__create__failure'.format(self.test_db_name)

        # Verify database does not yet exist.
        try:
            self.connector.query.execute('CREATE DATABASE {0};'.format(db_name))
        except MySQLdb.OperationalError:
            # Database already exists, as we want.
            pass

        # Check databases prior to test query. Verify expected database returned.
        results = self.connector.database.show()
        self.assertGreaterEqual(len(results), 1)
        self.assertIn(db_name, results)

        # Run test query.
        with self.assertRaises(ValueError):
            self.connector.database.create(db_name)

    def test__use_database__success(self):
        """
        Test `USE DATABASE` query, when database exists.
        """
        db_name = '{0}__use__success'.format(self.test_db_name)

        # Verify database exists.
        try:
            self.connector.query.execute('CREATE DATABASE {0};'.format(db_name))
        except MySQLdb.OperationalError:
            # Database already exists, as we want.
            pass

        # Check databases prior to test query. Verify expected database returned.
        results = self.connector.database.show()
        self.assertGreaterEqual(len(results), 1)
        self.assertIn(db_name, results)

        # Run test query.
        self.connector.database.use(db_name)

        # Check results of test query.
        results = self.connector.query.execute('SELECT DATABASE();')

        # Verify expected database returned.
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0][0], db_name)

    def test__use_database__failure(self):
        """
        Test `USE DATABASE` query, when database does not exist.
        """
        db_name = '{0}__use__failure'.format(self.test_db_name)

        # Verify database does not yet exist.
        try:
            self.connector.query.execute('DROP DATABASE {0};'.format(db_name))
        except MySQLdb.OperationalError:
            # Database does not exist, as we want.
            pass

        # Check databases prior to test query. Verify expected database did not return.
        results = self.connector.database.show()
        self.assertNotIn(db_name, results)

        # Run test query.
        with self.assertRaises(ValueError):
            self.connector.database.use(db_name)

    def test__delete_database__success(self):
        """
        Test `DROP DATABASE` query, when database exists.
        """
        db_name = '{0}__delete__success'.format(self.test_db_name)

        # Verify database does not yet exist.
        try:
            self.connector.query.execute('CREATE DATABASE {0};'.format(db_name))
        except MySQLdb.OperationalError:
            # Database already exists, as we want.
            pass

        # Check databases prior to test query. Verify expected database returned.
        results = self.connector.database.show()
        self.assertGreaterEqual(len(results), 1)
        self.assertIn(db_name, results)

        # Run test query.
        self.connector.database.delete(db_name)

        # Check databases after test query. Verify expected database did not return.
        results = self.connector.database.show()
        self.assertGreaterEqual(len(results), 1)
        self.assertNotIn(db_name, results)

    def test__delete_database__failure(self):
        """
        Test `DROP DATABASE` query, when database does not exist.
        """
        db_name = '{0}__delete__failure'.format(self.test_db_name)

        # Verify database does not yet exist.
        try:
            self.connector.query.execute('DROP DATABASE {0};'.format(db_name))
        except MySQLdb.OperationalError:
            # Database does not yet exist, as we want.
            pass

        # Check databases prior to test query. Verify expected database did not return.
        results = self.connector.database.show()
        self.assertNotIn(db_name, results)

        # Run test query.
        with self.assertRaises(ValueError):
            self.connector.database.delete(db_name)
