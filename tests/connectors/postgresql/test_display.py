"""
Tests for "display" logic of "PostgreSQL" DB Connector class.
"""

# System Imports.
import unittest

# User Imports.
from config import mysql_config, sqlite_config
from py_dbcn.connectors import MysqlDbConnector, PostgresqlDbConnector, SqliteDbConnector


class TestPostgresqlDisplay(unittest.TestCase):
    """
    Tests "PostgreSQL" DB Connector class display logic.
    """
    @classmethod
    def setUpClass(cls):
        # Run parent setup logic.
        super().setUpClass()
