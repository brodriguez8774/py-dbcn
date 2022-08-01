"""
Tests for "validate" logic of "MySQL" DB Connector class.
"""

# System Imports.

# User Imports.
from .test_core import TestMysqlDatabaseParent
from tests.connectors.core.test_validate import CoreValidateTestMixin


class TestMysqlValidate(TestMysqlDatabaseParent, CoreValidateTestMixin):
    """
    Tests "MySQL" DB Connector class validation logic.
    """
    @classmethod
    def setUpClass(cls):
        # Run parent setup logic.
        super().setUpClass()

        # Also call CoreValidateTestMixin setup logic.
        cls.set_up_class()
