"""
Tests for "utility" logic of "Core" DB Connector class.
"""

# System Imports.

# Internal Imports.


class CoreUtilsTestMixin:
    """
    Tests "Core" DB Connector class utility logic.
    """
    @classmethod
    def set_up_class(cls):
        """
        Acts as the equivalent of the UnitTesting "setUpClass()" function.

        However, since this is not inheriting from a given TestCase, calling the literal function
        here would override instead.
        """
        cls.test_db_name_start = cls.test_db_name_start.format(cls.db_type)
