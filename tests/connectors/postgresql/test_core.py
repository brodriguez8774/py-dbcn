"""
Initialization of "core" logic of "PostgreSQL" DB Connector class.
"""

# System Imports.
import psycopg2

# User Imports.
from config import postgresql_config
from py_dbcn.connectors import PostgresqlDbConnector
from tests.connectors.core.test_core import CoreTestParent


class TestPostgresqlDatabaseParent(CoreTestParent):
    """
    Initialization of "PostgreSQL" DB Connector parent class.
    """
    @classmethod
    def setUpClass(cls):
        # Run parent setup logic.
        super().setUpClass()

        # Initialize connector class to test.
        cls.connector = PostgresqlDbConnector(
            postgresql_config['host'],
            postgresql_config['port'],
            postgresql_config['user'],
            postgresql_config['password'],
            postgresql_config['name'],
            debug=True,
        )
        cls.db_type = cls.connector._config.db_type
        cls._implemented_db_types = cls.connector._config._implemented_db_types
        cls.db_error_handler = psycopg2
