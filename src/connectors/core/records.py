"""
Record/row/entry manipulation section of "Core" DB Connector class.

Contains generalized database connection logic.
Should be inherited by language-specific connectors.
"""

# System Imports.

# User Imports.
from src.logging import init_logging


# Import logger.
logger = init_logging(__name__)


class BaseRecords:
    """
    Abstract/generalized logic, for making record/row/entry queries.

    (As this project develops, logic will likely start here,
    and then be gradually moved to specific connectors as needed.)
    """
    def __init__(self, parent, *args, **kwargs):
        logger.debug('Generating related (core) Records class.')

        # Define connector root object.
        self._base = parent

        # Define provided direct parent object.
        self._parent = parent
