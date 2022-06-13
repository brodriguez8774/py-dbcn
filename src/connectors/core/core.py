"""
"Core" DB Connector class.

Contains generalized database connection logic.
Should be inherited by language-specific connectors.
"""

# System Imports.
from abc import ABC, abstractmethod

# User Imports.
from src.logging import init_logging
from .database import BaseDatabase
from .display import BaseDisplay
from .query import BaseQuery
from .records import BaseRecords
from .tables import BaseTables
from .validate import BaseValidate


# Import logger.
logger = init_logging(__name__)


class AbstractDbConnector(ABC):
    """
    Abstract/generalized database connector logic, that is universal to all database classes.

    (As this project develops, logic will likely start here,
    and then be gradually moved to specific connectors as needed.)
    """
    @abstractmethod
    def __init__(self, *args, debug=False, **kwargs):
        logger.debug('Generating (core) Connector class.')

        self._connection = None
        self._debug = debug

        # Create references to related subclasses.
        self.database = self._get_related_database_class()
        self.display = self._get_related_display_class()
        self.query = self._get_related_query_class()
        self.records = self._get_related_records_class()
        self.tables = self._get_related_tables_class()
        self.validate = self._get_related_validate_class()

    def __del__(self):
        """
        Close database connection on exit.
        """
        try:
            self._connection.close()
        except:
            pass

    def _get_related_database_class(self):
        """
        Overridable method to get the related "database functionality" class.
        """
        return BaseDatabase(self)

    def _get_related_display_class(self):
        """
        Overridable method to get the related "display functionality" class.
        """
        return BaseDisplay(self)

    def _get_related_query_class(self):
        """
        Overridable method to get the related "query functionality" class.
        """
        return BaseQuery(self)

    def _get_related_records_class(self):
        """
        Overridable method to get the related "record functionality" class.
        """
        return BaseRecords(self)

    def _get_related_tables_class(self):
        """
        Overridable method to get the related "tables functionality" class.
        """
        return BaseTables(self)

    def _get_related_validate_class(self):
        """
        Overridable method to get the related "validation functionality" class.
        """
        return BaseValidate(self)
