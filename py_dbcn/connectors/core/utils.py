"""
Utils section of "Core" DB Connector class.

Contains generalized database connection logic.
Should be inherited by language-specific connectors.
"""

# System Imports.

# Internal Imports.
from py_dbcn.logging import init_logging


# Import logger.
logger = init_logging(__name__)


class BaseUtils:
    """
    Abstract/generalized utility logic.

    (As this project develops, logic will likely start here,
    and then be gradually moved to specific connectors as needed.)
    """
    def __init__(self, parent, *args, **kwargs):
        logger.debug('Generating related (core) Utils class.')

        # Define connector root object.
        self._base = parent

        # Define provided direct parent object.
        self._parent = parent
