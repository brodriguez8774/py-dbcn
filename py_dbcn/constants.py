"""
Constant values for py-dbcn package.
"""

# Imports that may not be accessible, depending on local python environment setup.
# Database type imports.
try:
    import MySQLdb
    MYSQL_PRESENT = True
except ImportError:
    MYSQL_PRESENT = False
try:
    import psycopg2
    POSTGRESQL_PRESENT = True
except ImportError:
    POSTGRESQL_PRESENT = False

# Timezone imports.
try:
    from zoneinfo import ZoneInfo
    ZONEINFO_PRESENT = True
except ImportError:
    ZONEINFO_PRESENT = False
try:
    import pytz
    PYTZ_PRESENT = True
except ImportError:
    PYTZ_PRESENT = False
