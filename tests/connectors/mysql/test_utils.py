"""
Tests for "utility" logic of "MySQL" DB Connector class.
"""

# System Imports.
import datetime

# Internal Imports.
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

        # Define database name to use in tests.
        cls.test_db_name = '{0}test_utils'.format(cls.test_db_name_start)

        # Initialize database for tests.
        cls.connector.database.create(cls.test_db_name)
        cls.connector.database.use(cls.test_db_name)

        # Check that database has no tables.
        results = cls.connector.tables.show()
        if len(results) > 0:
            for result in results:
                cls.connector.tables.drop(result)

    def test__convert_timestamp_to_datetime__zoneinfo(self):
        """
        Tests for convert_timestamp_to_datetime() function.
        Located here because this appears to be MySQL-specific field types.
        """
        from zoneinfo import ZoneInfo

        utc_timezone = ZoneInfo('UTC')
        detroit_timezone = ZoneInfo('America/Detroit')

        # Determine timezone for MySQL server. This directly affects the timestamp value.
        sql_timezone = self.connector.query.execute('SELECT @@global.time_zone, @@session.time_zone;')
        if len(sql_timezone) == 1 and sql_timezone[0] == ('SYSTEM', 'SYSTEM'):
            # Is set to "system". Assume UTC for now.
            sql_timezone = utc_timezone
        else:
            raise NotImplemented(
                'TODO: Determine when this returns anything other than "SYSTEM" and handle accordingly.'
            )

        # Create table for test.
        table_name = 'test__timestamp_to_datetime'
        columns_clause = 'my_timestamp timestamp, my_datetime datetime'
        self.connector.tables.create(table_name, columns_clause)
        self.connector.tables.show()
        self.connector.tables.describe(table_name)

        # Get "now" in Python, and also insert into database.
        detroit_now = datetime.datetime.now(tz=detroit_timezone)
        utc_now = detroit_now.astimezone(utc_timezone)
        self.connector.records.insert(table_name, '((now()), (now()))')

        # Pull values as database created them.
        records = self.connector.records.select(table_name, 'my_timestamp')

        # # TODO: Until we add handling for non-"system" values, this section of the test technically does nothing.
        # # Convert to local MySQL timezone, then to utc.
        # results = self.connector.utils.convert_timestamp_to_datetime(records[0][0])
        #
        # print('results: {0}'.format(results))
        # print('\n\n\n\n')
        # local_datetime = records[0][0].replace(tzinfo=sql_timezone)
        # local_datetime = local_datetime.astimezone(utc_timezone)
        #
        # self.assertEqual(local_datetime, utc_now)
        # self.assertEqual(local_datetime, results)

        # TODO: Okay, test does things again starting here.
        # Generate a test value with Python, and convert using function.
        detroit_four_hours_prior = (detroit_now - datetime.timedelta(hours=4)).replace(tzinfo=None)
        utc_four_hours_prior = (utc_now - datetime.timedelta(hours=4)).replace(tzinfo=None)
        results = self.connector.utils.convert_timestamp_to_datetime(
            detroit_four_hours_prior,
            timezone=detroit_timezone,
        )
        self.assertEqual(utc_four_hours_prior, results)
