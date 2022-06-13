"""
Tests for "query" logic of "MySQL" DB Connector class.
"""

# System Imports.
import MySQLdb

# User Imports.
from .test_core import TestMysqlDatabaseParent


class TestMysqlQuery(TestMysqlDatabaseParent):
    """
    Tests "MySQL" DB Connector class query logic.
    """
    @classmethod
    def setUpClass(cls):
        # Run parent setup logic.
        super().setUpClass()
