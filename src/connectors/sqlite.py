"""
MySQL DB Connector class.
"""

# System Imports.
import sqlite3

# User Imports.
from .core import AbstractDbConnector
from src.logging import init_logging


# Import logger.
logger = init_logging(__name__)


class SqliteConnector(AbstractDbConnector):
    """
    Object to manage connections to SqLite databases.
    """
    def __init__(self, db_location, debug=False):
        # Call parent logic.
        super().__init__(debug=debug)

        # Initialize database connection.
        self.connection = sqlite3.connect(db_location)
        logger.info('Created Sqlilte database connection.')
