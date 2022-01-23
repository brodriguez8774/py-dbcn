"""
PostgreSQL DB Connector class.

Contains database connection logic specific to PostgreSQL databases.
"""

# System Imports.

# User Imports.
from .database import PostgresqlDatabase
from .display import PostgresqlDisplay
from .query import PostgresqlQuery
from .tables import PostgresqlTables
from .validate import PostgresqlValidate
from src.connectors.core import AbstractDbConnector
from src.logging import init_logging


# Import logger.
logger = init_logging(__name__)


class PostgresqlDbConnector(AbstractDbConnector):
    """
    Abstract connector for database and
    """
    def __init__(self, *args, debug=False, **kwargs):
        # Call parent logic.
        super().__init__(*args, debug=debug, **kwargs)

        # Initialize database connection.
        # self.connection = MySQLdb.connect(host=db_host, port=db_port, user=db_user, password=db_pass, db=db_name)
        logger.info('Created PostgreSQL database connection.')

    def _get_related_database_class(self):
        """
        Overridable method to get the related "database functionality" class.
        """
        return PostgresqlDatabase(self)

    def _get_related_display_class(self):
        """
        Overridable method to get the related "display functionality" class.
        """
        return PostgresqlDisplay(self)

    def _get_related_query_class(self):
        """
        Overridable method to get the related "query functionality" class.
        """
        return PostgresqlQuery(self)

    def _get_related_tables_class(self):
        """
        Overridable method to get the related "tables functionality" class.
        """
        return PostgresqlTables(self)

    def _get_related_validate_class(self):
        """
        Overridable method to get the related "validation functionality" class.
        """
        return PostgresqlValidate(self)
