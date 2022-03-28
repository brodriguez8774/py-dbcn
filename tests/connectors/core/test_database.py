"""
Tests for "database" logic of "Core" DB Connector class.
"""

# System Imports.
import unittest

# User Imports.
from config import mysql_config, sqlite_config
from src.connectors import MysqlDbConnector, PostgresqlDbConnector, SqliteDbConnector


class TestCoreDatabase(unittest.TestCase):
    """
    Tests "Core" DB Connector class database logic.
    """
    @classmethod
    def setUpClass(cls):
        # Run parent setup logic.
        super().setUpClass()

    def test__create_database__success(self):
        """"""

    def test__create_database__failure(self):
        """"""
