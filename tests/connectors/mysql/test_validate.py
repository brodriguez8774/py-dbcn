"""
Tests for "validate" logic of "MySQL" DB Connector class.
"""

# System Imports.
import unittest

# User Imports.
from config import mysql_config, sqlite_config
from py_dbcn.connectors import MysqlDbConnector, PostgresqlDbConnector, SqliteDbConnector
from py_dbcn.connectors.core.validate import BaseValidate


class TestMysqlValidate(unittest.TestCase):
    """
    Tests "MySQL" DB Connector class validation logic.
    """
    @classmethod
    def setUpClass(cls):
        # Run parent setup logic.
        super().setUpClass()
