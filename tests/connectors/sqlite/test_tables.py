"""
Tests for "tables" logic of "SqLite" DB Connector class.
"""

# System Imports.
import unittest

# Internal Imports.
from config import mysql_config, sqlite_config
from py_dbcn.connectors import MysqlDbConnector, PostgresqlDbConnector, SqliteDbConnector


class TestSqliteTables(unittest.TestCase):
    """
    Tests "SqLite" DB Connector class table logic.
    """
    @classmethod
    def setUpClass(cls):
        # Run parent setup logic.
        super().setUpClass()
