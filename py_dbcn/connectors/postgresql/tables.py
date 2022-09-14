"""
Table section of "PostgreSQL" DB Connector class.

Contains database connection logic specific to PostgreSQL databases.
"""

# System Imports.
import textwrap

# Internal Imports.
from py_dbcn.connectors.core.tables import BaseTables
from py_dbcn.logging import init_logging


# Import logger.
logger = init_logging(__name__)


class PostgresqlTables(BaseTables):
    """
    Logic for making table queries, for PostgreSQL databases.
    """
    def __init__(self, parent, *args, **kwargs):
        # Call parent logic.
        super().__init__(parent, *args, **kwargs)

        logger.debug('Generating related (PostgreSQL) Tables class.')

        # Initialize variables.
        # StackOverflow suggested each of these in different answers.
        # Unsure of which one is better/worse, and what the differences mean.
        self._show_tables_query = textwrap.dedent(
            """
            SELECT table_name FROM information_schema.tables
            WHERE table_schema = 'public';
            """

            # "SELECT table_schema || '.' || table_name "
            # "FROM information_schema.tables "
            # "WHERE table_type = 'BASE TABLE' "
            # "AND table_schema NOT IN ('pg_catalog', 'information_schema');"

            # "SELECT * FROM pg_catalog.pg_tables "
            # "WHERE schemaname != 'pg_catalog' AND schemaname != 'information_schema';"
        ).strip()
        self._describe_table_query = textwrap.dedent(
            """
            SELECT * FROM information_schema.columns
            WHERE (table_schema = 'public' AND table_name = '{0}');
            """
        ).strip()
