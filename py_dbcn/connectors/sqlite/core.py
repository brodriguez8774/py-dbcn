"""
SqLite DB Connector class.

Contains database connection logic specific to SqLite databases.
"""

# System Imports.

# Third-party Imports.
import sqlite3

# Internal Imports.
from .database import SqliteDatabase
from .display import SqliteDisplay
from .query import SqliteQuery
from .records import SqliteRecords
from .tables import SqliteTables
from .validate import SqliteValidate
from py_dbcn.connectors.core import AbstractDbConnector
from py_dbcn.logging import init_logging


# Import logger.
logger = init_logging(__name__)


class SqliteDbConnector(AbstractDbConnector):
    """
    Database connector logic for SqLite databases.
    """
    def __init__(self, db_location, *args, debug=False, **kwargs):
        # Call parent logic.
        super().__init__(*args, debug=debug, **kwargs)

        # Initialize database connection.
        self.connection = sqlite3.connect(db_location)
        logger.info('Created Sqlilte database connection.')

    def _get_related_database_class(self):
        """
        Overridable method to get the related "database functionality" class.
        """
        return SqliteDatabase(self)

    def _get_related_display_class(self):
        """
        Overridable method to get the related "display functionality" class.
        """
        return SqliteDisplay(self)

    def _get_related_query_class(self):
        """
        Overridable method to get the related "query functionality" class.
        """
        return SqliteQuery(self)

    def _get_related_records_class(self):
        """
        Overridable method to get the related "records functionality" class.
        """
        return SqliteRecords(self)

    def _get_related_tables_class(self):
        """
        Overridable method to get the related "tables functionality" class.
        """
        return SqliteTables(self)

    def _get_related_validate_class(self):
        """
        Overridable method to get the related "validation functionality" class.
        """
        return SqliteValidate(self)
