"""
Tests for "tables" logic of "PostgreSQL" DB Connector class.
"""

# System Imports.
import textwrap

# User Imports.
from .test_core import TestPostgresqlDatabaseParent
from tests.connectors.core.test_tables import CoreTablesTestMixin


class TestPostgresqlTables(TestPostgresqlDatabaseParent, CoreTablesTestMixin):
    """
    Tests "PostgreSQL" DB Connector class table logic.
    """
    @classmethod
    def setUpClass(cls):
        # Run parent setup logic.
        super().setUpClass()

        # Also call CoreTestMixin setup logic.
        cls.set_up_class()

        # Define database name to use in tests.
        cls.test_db_name = '{0}test_tables'.format(cls.test_db_name_start)

        # Initialize database for tests.
        cls.connector.database.create(cls.test_db_name)
        cls.connector.database.use(cls.test_db_name)

        # Check that database has no tables.
        results = cls.connector.tables.show()
        if len(results) > 0:
            for result in results:
                cls.connector.tables.drop(result)

        # Define database-specific query values.
        cls._basic_table_columns = textwrap.dedent(
            """
            (
                id serial PRIMARY KEY
            )
            """
        ).strip()
        cls._columns_query = textwrap.dedent(
            """
            (
                id serial PRIMARY KEY,
                name VARCHAR(100),
                description VARCHAR(100)
            )
            """
        ).strip()
