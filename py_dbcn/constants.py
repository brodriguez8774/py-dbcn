"""
Constant values for py-dbcn package.
"""

# Imports that may not be accessible, depending on local python environment setup.
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
