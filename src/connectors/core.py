"""
Core DB Connector class.
"""

# System Imports.
from abc import ABC, abstractmethod

# User Imports.
from src.logging import init_logging


# Import logger.
logger = init_logging(__name__)


class AbstractDbConnector():
    """
    Abstract connector for database and
    """
    def __init__(self, debug=False):
        logger.debug('Generating (core) Connector class.')
        self.connection = None
        self._debug = debug

        # Create references to related subclasses.
        self.database = self._get_related_database_class()
        self.display = self._get_related_display_class()
        self.query = self._get_related_query_class()
        self.validate = self._get_related_validate_class()

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

    def _get_related_validate_class(self):
        """
        Overridable method to get the related "validation functionality" class.
        """
        return BaseValidate(self)


class BaseDatabase():
    """

    """
    def __init__(self, parent):
        logger.debug('Generating related (core) Database class.')
        self._base = parent

    def use(self, db_name):
        """
        Selects given database for use.
        """
        query = 'USE {0};'.format(db_name)
        self._base.query.execute(query)


class BaseDisplay():
    """

    """
    def __init__(self, parent):
        logger.debug('Generating related (core) Display class.')
        self._base = parent


class BaseQuery():
    """

    """
    def __init__(self, parent):
        logger.debug('Generating related (core) Query class.')
        self._base = parent

    def execute(self, query):
        """"""
        logger.info(query)


class BaseValidate():
    """

    """
    def __init__(self, parent):
        logger.debug('Generating related (core) Validate class.')
        self._base = parent
