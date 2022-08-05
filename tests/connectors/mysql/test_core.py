"""
Initialization of "core" logic of "MySQL" DB Connector class.
"""

# System Imports.

# User Imports.
from config import mysql_config
from py_dbcn.connectors import MysqlDbConnector
from tests.connectors.core.test_core import CoreTestParent


class TestMysqlDatabaseParent(CoreTestParent):
    """
    Initialization of "MySQL" DB Connector class database logic.
    """
    @classmethod
    def setUpClass(cls):
        # Run parent setup logic.
        super().setUpClass()

        # Initialize connector class to test.
        cls.connector = MysqlDbConnector(
            mysql_config['host'],
            mysql_config['port'],
            mysql_config['user'],
            mysql_config['password'],
            mysql_config['name'],
            debug=True,
        )
        cls.db_type = 'MySQL'
