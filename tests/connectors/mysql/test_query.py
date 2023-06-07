"""
Tests for "query" logic of "MySQL" DB Connector class.
"""

# System Imports.

# Internal Imports.
from .test_core import TestMysqlDatabaseParent
from tests.connectors.core.test_query import CoreQueryTestMixin


class TestMysqlQuery(TestMysqlDatabaseParent, CoreQueryTestMixin):
    """
    Tests "MySQL" DB Connector class query logic.
    """
    @classmethod
    def setUpClass(cls):
        # Run parent setup logic.
        super().setUpClass()

        # Also call CoreTestMixin setup logic.
        cls.set_up_class()

        # Define database name to use in tests.
        cls.test_db_name = '{0}test_query'.format(cls.test_db_name_start)

        # Ensure database does not currently exists.
        # Guarantees tests are done from a consistent state.
        try:
            cls.connector.database.drop(cls.test_db_name, display_query=False, display_results=False)
        except cls.connector.errors.database_does_not_exist:
            # Database already exists, as we want.
            pass

        # Create desired database.
        cls.connector.database.create(cls.test_db_name)

        # Select desired database.
        cls.connector.database.use(cls.test_db_name)

        # Check that database has no tables.
        results = cls.connector.tables.show()
        if len(results) > 0:
            for result in results:
                cls.connector.tables.drop(result)
