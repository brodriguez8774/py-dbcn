"""
Tests for "clauses" logic of "MySQL" DB Connector class.
"""

# System Imports.

# Internal Imports.
from .test_core import TestMysqlDatabaseParent
from tests.connectors.core.test_clauses import CoreClauseTestMixin


class TestMysqlDatabase(TestMysqlDatabaseParent, CoreClauseTestMixin):
    """
    Tests "MySQL" DB Connector class clause logic.
    """
    @classmethod
    def setUpClass(cls):
        # Run parent setup logic.
        super().setUpClass()

        # Also call CoreTestMixin setup logic.
        cls.set_up_class()

        # Define database name to use in tests.
        cls.test_db_name = '{0}test_database'.format(cls.test_db_name_start)
