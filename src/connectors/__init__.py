"""
Imports database connectors from "connectors" folder.
Makes project imports to this folder behave like a standard single file.
"""

from .sqlite import SqliteConnector
from .mysql import MySqlConnector
