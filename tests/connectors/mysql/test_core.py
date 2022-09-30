"""
Initialization of "core" logic of "MySQL" DB Connector class.
"""

# Standard Imports.
import unittest

# Internal Imports.
from tests.connectors.core.test_core import CoreTestParent


# Skip all imports if MYSQL_PRESENT is not present on system.
from py_dbcn.constants import MYSQL_PRESENT


# MySQL Imports.
if MYSQL_PRESENT:
    # System Imports.
    import MySQLdb

    # Internal Imports.
    from config import mysql_config
    from py_dbcn.connectors import MysqlDbConnector


@unittest.skipUnless(MYSQL_PRESENT, 'Failed to import MySQL. Assuming not installed. Skipping tests.')
class TestMysqlDatabaseParent(CoreTestParent):
    """
    Initialization of "MySQL" DB Connector parent class.
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
        cls.db_type = cls.connector._config.db_type
        cls._implemented_db_types = cls.connector._config._implemented_db_types
        cls.db_error_handler = cls.connector.errors.handler
