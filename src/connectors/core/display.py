"""
Display section of "Core" DB Connector class.

Contains generalized database connection logic.
Should be inherited by language-specific connectors.
"""

# System Imports.

# User Imports.
from src.logging import init_logging


# Import logger.
logger = init_logging(__name__)


class BaseDisplay():
    """

    """
    def __init__(self, parent):
        logger.debug('Generating related (core) Display class.')
        self._base = parent
