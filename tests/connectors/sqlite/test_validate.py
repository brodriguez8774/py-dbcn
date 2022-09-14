"""
Tests for "validate" logic of "SqLite" DB Connector class.
"""

# System Imports.
import unittest

# Internal Imports.
from config import mysql_config, sqlite_config
from py_dbcn.connectors import MysqlDbConnector, PostgresqlDbConnector, SqliteDbConnector
from py_dbcn.connectors.core.validate import BaseValidate


class TestSqliteValidate(unittest.TestCase):
    """
    Tests "SqLite" DB Connector class validation logic.
    """
    @classmethod
    def setUpClass(cls):
        # Run parent setup logic.
        super().setUpClass()
