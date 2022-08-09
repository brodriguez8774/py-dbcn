"""
Example of project config file, for defining database connection settings.

If modifying these values at all, please copy to a new "config.py" file and edit values there.
"""

# SqLite connection values.
sqlite_config = {
    'location': 'db.sqlite3'
}


# MySQL connection values.
mysql_config = {
    'host': '127.0.0.1',
    'port': '3306',
    'name': 'db_name',
    'user': 'db_user',
    'password': 'db_pass',
}


# PostgreSQL connection values.
postgresql_config = {
    'host': '127.0.0.1',
    'port': '3306',
    'name': 'db_name',
    'user': 'db_user',
    'password': 'db_pass',
}
