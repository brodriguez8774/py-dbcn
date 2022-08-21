"""
Tests for "tables" logic of "MySQL" DB Connector class.
"""

# System Imports.

# User Imports.
import textwrap

from .test_core import TestMysqlDatabaseParent
from tests.connectors.core.test_tables import CoreTablesTestMixin


class TestMysqlTables(TestMysqlDatabaseParent, CoreTablesTestMixin):
    """
    Tests "MySQL" DB Connector class table logic.
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
                id INT(11) NOT NULL AUTO_INCREMENT,
                PRIMARY KEY (id)
            )
            """
        ).strip()
        cls._columns_query = textwrap.dedent(
            """
            (
                id INT NOT NULL AUTO_INCREMENT,
                name VARCHAR(100),
                description VARCHAR(100),
                PRIMARY KEY ( id )
            )
            """
        ).strip()
