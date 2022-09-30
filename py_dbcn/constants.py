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


# Color output imports.
try:
    from colorama import Back, Fore, Style
    COLORAMA_PRESENT = True
except ImportError:
    COLORAMA_PRESENT = False


# Underline style definition for debug printing.
UNDERLINE = '\u001b[4m'
UNDERLINE_RESET = '\u001b[0m'


# General output format settings.
OUTPUT_QUERY = str('{0}'.format(Fore.MAGENTA) if COLORAMA_PRESENT else '')
OUTPUT_RESULTS = str('{0}'.format(Fore.BLUE) if COLORAMA_PRESENT else '')
OUTPUT_ERROR = str('{0}{1}{2}'.format(Fore.RED, Back.RESET, Style.NORMAL) if COLORAMA_PRESENT else '')
OUTPUT_EXPECTED_MATCH = str('{0}{1}{2}'.format(Fore.GREEN, Back.RESET, Style.NORMAL) if COLORAMA_PRESENT else '')
OUTPUT_EXPECTED_ERROR = str('{0}{1}{2}'.format(Fore.BLACK, Back.GREEN, Style.NORMAL) if COLORAMA_PRESENT else '')
OUTPUT_ACTUALS_MATCH = str('{0}{1}{2}'.format(Fore.RED, Back.RESET, Style.NORMAL) if COLORAMA_PRESENT else '')
OUTPUT_ACTUALS_ERROR = str('{0}{1}{2}'.format(Fore.BLACK, Back.RED, Style.NORMAL) if COLORAMA_PRESENT else '')
OUTPUT_EMPHASIS = str((Style.BRIGHT if COLORAMA_PRESENT else '') + UNDERLINE)
OUTPUT_RESET = str(Style.RESET_ALL if COLORAMA_PRESENT else UNDERLINE_RESET)
