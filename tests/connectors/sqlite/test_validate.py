"""
Tests for "validate" logic of "SqLite" DB Connector class.
"""

# System Imports.
import unittest

# User Imports.
from config import mysql_config, sqlite_config
from src.connectors import MysqlDbConnector, PostgresqlDbConnector, SqliteDbConnector
from src.connectors.core.validate import BaseValidate


class TestSqliteValidate(unittest.TestCase):
    """
    Tests "SqLite" DB Connector class validation logic.
    """
    @classmethod
    def setUpClass(cls):
        # Run parent setup logic.
        super().setUpClass()
