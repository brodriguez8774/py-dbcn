"""
MySQL DB Connector class.

Contains database connection logic specific to MySQL databases.
"""

# System Imports.
import MySQLdb

# User Imports.
from .database import MysqlDatabase
from .display import MysqlDisplay
from .query import MysqlQuery
from .records import MysqlRecords
from .tables import MysqlTables
from .validate import MysqlValidate
from src.connectors.core import AbstractDbConnector
from src.logging import init_logging


# Import logger.
logger = init_logging(__name__)


class MysqlDbConnector(AbstractDbConnector):
    """
    Database connector logic for MySQL databases.
    """
    def __init__(self, db_host, db_port, db_user, db_pass, db_name, *args, debug=False, **kwargs):
        db_port = int(db_port)

        # Call parent logic.
        super().__init__(*args, debug=debug, **kwargs)

        # Initialize database connection.
        self._connection = MySQLdb.connect(host=db_host, port=db_port, user=db_user, password=db_pass, db=db_name)
        logger.info('Created MySQL database connection.')

    def _get_related_database_class(self):
        """
        Overridable method to get the related "database functionality" class.
        """
        return MysqlDatabase(self)

    def _get_related_display_class(self):
        """
        Overridable method to get the related "display functionality" class.
        """
        return MysqlDisplay(self)

    def _get_related_query_class(self):
        """
        Overridable method to get the related "query functionality" class.
        """
        return MysqlQuery(self)

    def _get_related_records_class(self):
        """
        Overridable method to get the related "records functionality" class.
        """
        return MysqlRecords(self)

    def _get_related_tables_class(self):
        """
        Overridable method to get the related "tables functionality" class.
        """
        return MysqlTables(self)

    def _get_related_validate_class(self):
        """
        Overridable method to get the related "validation functionality" class.
        """
        return MysqlValidate(self)
