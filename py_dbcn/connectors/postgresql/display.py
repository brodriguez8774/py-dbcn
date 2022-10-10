"""
Display section of "PostgreSQL" DB Connector class.

Contains database connection logic specific to PostgreSQL databases.
"""

# System Imports.
import textwrap

# Internal Imports.
from py_dbcn.connectors.core.display import BaseDisplay
from py_dbcn.logging import init_logging


# Import logger.
logger = init_logging(__name__)


class PostgresqlDisplay(BaseDisplay):
    """
    Logic for displaying queries and other project output in prettier format, for PostgreSQL databases.
    """
    def __init__(self, parent, *args, **kwargs):
        # Call parent logic.
        super().__init__(parent, *args, **kwargs)

        logger.debug('Generating related (PostgreSQL) Display class.')

        self.max_col_length_query = textwrap.dedent(
            """
            SELECT MAX(LENGTH(CAST({2}{0}{2} as text))) FROM {1};
            """.strip()
        )
