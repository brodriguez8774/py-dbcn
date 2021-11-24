"""
MySQL DB Connector class.
"""

# System Imports.
import MySQLdb

# User Imports.
from .core import AbstractDbConnector
from src.logging import init_logging


# Import logger.
logger = init_logging(__name__)


class MySqlConnector(AbstractDbConnector):
    """
    Object to manage connections to MySQL databases.
    """
    def __init__(self, db_host, db_port, db_user, db_pass, db_name, debug=False):
        db_port = int(db_port)

        # Call parent logic.
        super().__init__(debug=debug)

        # Initialize database connection.
        self.connection = MySQLdb.connect(host=db_host, port=db_port, user=db_user, password=db_pass, db=db_name)
        logger.info('Created MySQL database connection.')
