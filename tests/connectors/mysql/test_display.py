"""
Tests for "display" logic of "MySQL" DB Connector class.
"""

# System Imports.

# User Imports.
from .test_core import TestMysqlDatabaseParent
from .expected_display_output import ExpectedOutput
from tests.connectors.core.test_display import (
    CoreDisplayBaseTestMixin,
    CoreDisplayTablesTestMixin,
    CoreDisplayRecordsMixin,
)


class TestMysqlDisplayCore(TestMysqlDatabaseParent, CoreDisplayBaseTestMixin):
    """
    Tests "MySQL" DB Connector class display logic.

    Specifically tests logic defined in base display class.
    """
    @classmethod
    def setUpClass(cls):
        # Run parent setup logic.
        super().setUpClass()

        # Also call CoreTestMixin setup logic.
        cls.set_up_class()

        # Define database name to use in tests.
        cls.test_db_name = '{0}test_display__core'.format(cls.test_db_name_start)

        # Initialize database for tests.
        cls.connector.database.create(cls.test_db_name)
        cls.connector.database.use(cls.test_db_name)

        # Check that database has no tables.
        results = cls.connector.tables.show()
        if len(results) > 0:
            for result in results:
                cls.connector.tables.drop(result)

        # Define expected output to compare against.
        cls.expected_output = ExpectedOutput


class TestMysqlDisplayTables(TestMysqlDatabaseParent, CoreDisplayTablesTestMixin):
    """
    Tests "MySQL" DB Connector class display logic.

    Specifically tests logic defined in "tables" display subclass.
    """
    @classmethod
    def setUpClass(cls):
        # Run parent setup logic.
        super().setUpClass()

        # Also call CoreTestMixin setup logic.
        cls.set_up_class()

        # Define database name to use in tests.
        cls.test_db_name = '{0}test_display__tables'.format(cls.test_db_name_start)

        # Initialize database for tests.
        cls.connector.database.create(cls.test_db_name)
        cls.connector.database.use(cls.test_db_name)

        # Check that database has no tables.
        results = cls.connector.tables.show()
        if len(results) > 0:
            for result in results:
                cls.connector.tables.drop(result)

        # Define expected output to compare against.
        cls.expected_output = ExpectedOutput


class TestMysqlDisplayRecords(TestMysqlDatabaseParent, CoreDisplayRecordsMixin):
    """
    Tests "MySQL" DB Connector class display logic.

    Specifically tests logic defined in "records" display subclass.
    """
    @classmethod
    def setUpClass(cls):
        # Run parent setup logic.
        super().setUpClass()

        # Also call CoreTestMixin setup logic.
        cls.set_up_class()

        # Define database name to use in tests.
        cls.test_db_name = '{0}test_display__records'.format(cls.test_db_name_start)

        # Initialize database for tests.
        cls.connector.database.create(cls.test_db_name)
        cls.connector.database.use(cls.test_db_name)

        # Check that database has no tables.
        results = cls.connector.tables.show()
        if len(results) > 0:
            for result in results:
                cls.connector.tables.drop(result)

        # Define expected output to compare against.
        cls.expected_output = ExpectedOutput
