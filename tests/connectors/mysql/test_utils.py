"""
Tests for "utility" logic of "MySQL" DB Connector class.
"""

# System Imports.

# User Imports.
from .test_core import TestMysqlDatabaseParent
from tests.connectors.core.test_utils import CoreUtilsTestMixin


class TestMysqlUtils(TestMysqlDatabaseParent, CoreUtilsTestMixin):
    """
    Tests "MySQL" DB Connector class utility logic.
    """
    @classmethod
    def setUpClass(cls):
        # Run parent setup logic.
        super().setUpClass()

        # Also call CoreUtilsTestMixin setup logic.
        cls.set_up_class()
