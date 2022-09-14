"""
Utils section of "MySQL" DB Connector class.

Contains database connection logic specific to MySQL databases.
"""

# System Imports.

# Internal Imports.
from py_dbcn.connectors.core.utils import BaseUtils
from py_dbcn.constants import PYTZ_PRESENT, ZONEINFO_PRESENT
from py_dbcn.logging import init_logging


# Import logger.
logger = init_logging(__name__)


class MysqlUtils(BaseUtils):
    """
    Extra utility logic, for MySQL databases.
    """
    def __init__(self, parent, *args, **kwargs):
        # Call parent logic.
        super().__init__(parent, *args, **kwargs)

        logger.debug('Generating related (MySQL) Utils class.')

    def convert_timestamp_to_datetime(self, timestamp, timezone='UTC'):
        """
        Converts passed MySQL timestamp into a MySQL datetime.
        Note that datetime has a larger range and thus is probably safer to use.

        Timestamp range: '1970-01-01 00:00:01' UTC to '2038-01-09 03:14:07' UTC
        Datetime range: '1000-01-01 00:00:00' to '9999-12-31 23:59:59'

        Timestamps also pull as whatever the local database's timezone is.
        Where datetimes will always pull as UTC format.

        Generally, it's probably better to have the backend be in UTC, and convert for frontend display if needed.
        So datetime is just all-around preferred.

        :param timestamp: Timestamp to convert.
        :param timezone: Timezone that stamp is based in. Assumes UTC by default.
        :return: Naive datetime object. But aligned to UTC timezone.
        """
        # Verify either pytz or zoneinfo is present in local python environment.
        if not PYTZ_PRESENT and not ZONEINFO_PRESENT:
            raise SystemError('Function requires either Pytz or Zoneinfo to be present. Found neither.')

        logger.debug('Timestamp: {0}'.format(timestamp))

        # Create statement.
        query = 'SELECT from_unixtime( UNIX_TIMESTAMP( "{0}" ) )'.format(timestamp)

        # Execute statement.
        results = self._base.query.execute(query, display_query=False)
        unaware_datetime = results[0][0]
        logger.debug('Unaware time: {0}'.format(unaware_datetime))

        # Attempt zoneinfo first if both are installed, as it's expected to fully replace pytz.
        if ZONEINFO_PRESENT:
            # Zoneinfo is present.
            from zoneinfo import ZoneInfo

            if isinstance(timezone, ZoneInfo):
                local_timezone = timezone
            else:
                local_timezone = ZoneInfo(timezone)
            utc_timezone = ZoneInfo('UTC')

            # Convert to aware datetime, using provided local timezone location.
            aware_datetime = unaware_datetime.replace(tzinfo=local_timezone)

            # Convert from local to UTC.
            aware_datetime = aware_datetime.astimezone(utc_timezone)
            logger.debug('Aware time: {0}'.format(aware_datetime))

            # Remove timezone info, so that it can be stored in the database.
            naive_datetime = aware_datetime.replace(tzinfo=None)
            logger.debug('Naive time: {0}'.format(naive_datetime))

        else:
            # Fall back to pytz.
            import pytz

            # Convert to aware datetime, using provided local timezone location.
            aware_datetime = pytz.timezone(timezone).localize(unaware_datetime)

            # Convert from local to UTC.
            aware_datetime = aware_datetime.astimezone(pytz.timezone('UTC'))
            logger.debug('Aware time: {0}'.format(aware_datetime))

            # Remove timezone info, so that it can be stored in the database.
            naive_datetime = aware_datetime.replace(tzinfo=None)
            logger.debug('Naive time: {0}'.format(naive_datetime))

        # Return calculated value.
        return naive_datetime
