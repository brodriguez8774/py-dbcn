"""
Tests for "display" logic of "SqLite" DB Connector class.
"""

# System Imports.
import unittest

# User Imports.
from config import mysql_config, sqlite_config
from src.connectors import MysqlDbConnector, PostgresqlDbConnector, SqliteDbConnector


class TestSqliteDisplay(unittest.TestCase):
    """
    Tests "SqLite" DB Connector class display logic.
    """
    @classmethod
    def setUpClass(cls):
        # Run parent setup logic.
        super().setUpClass()
