"""
Imports database connectors from "connectors" folder.
Makes project imports to this folder behave like a standard single file.
"""

from py_dbcn.constants import MYSQL_PRESENT, POSTGRESQL_PRESENT


if MYSQL_PRESENT:
    from .mysql import MysqlDbConnector
else:
    # Project likely does not have MySQLdb package installed.
    # This is okay, as we don't want this logic as a hard requirement to use this library.

    # However, we do want to define a dummy class to give feedback errors.
    class MysqlDbConnector:
        err_msg = """
        Cannot use MysqlDbConnector class without "MySQLdb" package installed.
        Installing this package also requires having MySQL installed on your system.
        """

        @classmethod
        def setUpClass(cls):
            raise Exception(cls.err_msg)

        def setUp(self):
            raise Exception(self.err_msg)

        def __int__(self):
            raise Exception(self.err_msg)


if POSTGRESQL_PRESENT:
    from .postgresql import PostgresqlDbConnector
else:
    # Project likely does not have MySQLdb package installed.
    # This is okay, as we don't want this logic as a hard requirement to use this library.

    # However, we do want to define a dummy class to give feedback errors.
    class PostgresqlDbConnector:
        err_msg = """
        Cannot use PostgresqlDbConnector class without "psycopg2-binary" package installed.
        Installing this package also requires having PostgreSQL installed on your system.
        """

        @classmethod
        def setUpClass(cls):
            raise Exception(cls.err_msg)

        def setUp(self):
            raise Exception(self.err_msg)

        def __int__(self):
            raise Exception(self.err_msg)


from .sqlite import SqliteDbConnector
