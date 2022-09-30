"""
Tests for "database" logic of "MySQL" DB Connector class.
"""

# System Imports.

# Internal Imports.
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

    def test_error_catch_types(self):
        """Tests to ensure database ERROR types are properly caught.

        Ex: MySQL and PostgreSQL interfaces do not catch "Database does not exist" errors the same.
            These tests make sure this error (and others) are properly caught, regardless of what database is
            being called.
        """
        # Call parent logic.
        super().test_error_catch_types()

        with self.subTest('Verify handling when database does not exist'):
            # Make sure we're using a database name that is not yet created.
            db_name = 'NewDatabaseName'
            results = self.connector.database.show()
            if db_name in results:
                raise AssertionError('Database already present. Incorrect name provided.')

            # Check that we use the correct handler.
            with self.assertRaises(self.connector.errors.database_does_not_exist):
                self.connector.query.execute('DROP DATABASE {0};'.format(db_name))

        with self.subTest('Verify handling when database already exists'):
            # Make sure we're using a database name that is already created.
            db_name = 'test_database'
            results = self.connector.database.show()
            if db_name not in results:
                raise AssertionError('Database not yet present. Incorrect name provided.')

            # Check that we use the correct handler.
            with self.assertRaises(self.connector.errors.database_already_exists):
                self.connector.query.execute('CREATE DATABASE {0};'.format(db_name))
