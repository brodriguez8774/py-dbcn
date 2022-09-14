"""
Tests for "query" logic of "PostgreSQL" DB Connector class.
"""

# System Imports.

# Internal Imports.
from .test_core import TestPostgresqlDatabaseParent
from tests.connectors.core.test_query import CoreQueryTestMixin


class TestPostgresqlQuery(TestPostgresqlDatabaseParent, CoreQueryTestMixin):
    """
    Tests "PostgreSQL" DB Connector class query logic.
    """
    @classmethod
    def setUpClass(cls):
        # Run parent setup logic.
        super().setUpClass()

        # Also call CoreTestMixin setup logic.
        cls.set_up_class()

        # Define database name to use in tests.
        cls.test_db_name = '{0}test_query'.format(cls.test_db_name_start)

        # Initialize database for tests.
        cls.connector.database.create(cls.test_db_name)
        cls.connector.database.use(cls.test_db_name)

        # Check that database has no tables.
        results = cls.connector.tables.show()
        if len(results) > 0:
            for result in results:
                cls.connector.tables.drop(result)
