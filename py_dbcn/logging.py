"""
Custom Python logger, defined via a dictionary of logging settings.

https://git.brandon-rodriguez.com/python/custom_logger
Version 1.1
"""


# System Imports.
import pathlib, sys
import logging.config


# Logging Variables.
this = sys.modules[__name__]
this.settings = None
project_dir = pathlib.Path().absolute()
this.logging_directory = project_dir.joinpath('py_dbcn/logs')
this.logging_class = 'logging.handlers.RotatingFileHandler'
this.logging_max_bytes = 1024 * 1024 * 10    # Max log file size of 10 MB.
this.logging_backup_count = 10               # Keep 10 log files before overwriting.


# region User Logging Settings
# These functions are separated to make logging modification easier for the end user.

def get_logging_settings():
    """
    Returns an instance of the logging settings dictionary.
    """
    return {
        'version': 1,
        'filters': {},
        'formatters': {
            # Minimal logging. Only includes message.
            # Generally meant for terminal "end user" interface display.
            'minimal': {
                'format': '%(message)s',
            },
            # Simple logging. Includes message type and actual message.
            # Generally meant for console logging.
            'simple': {
                'format': '[%(levelname)s] [%(filename)s %(lineno)d]: %(message)s',
            },
            # Basic logging. Includes date, message type, file originated, and actual message.
            # Generally meant for file logging.
            'standard': {
                'format': '%(asctime)s [%(levelname)s] [%(name)s %(lineno)d]: %(message)s',
            },
            # Verbose logging. Includes standard plus the process number and thread id.
            # For when you wanna be really verbose.
            'verbose': {
                'format': '%(asctime)s [%(levelname)s] [%(name)s %(lineno)d] || %(process)d %(thread)d || %(message)s'
            },
        },
        'handlers': {
            # Sends log message to the void. May be useful for debugging.
            'null': {
                'class': 'logging.NullHandler',
            },
            # To console.
            'console': {
                'level': 'INFO',
                'class': 'logging.StreamHandler',
                'formatter': 'minimal',
            },
            # Debug Level - To file.
            'file_debug': {
                'level': 'DEBUG',
                'class': this.logging_class,
                'filename': this.logging_directory.joinpath('debug.log'),
                'maxBytes': this.logging_max_bytes,
                'backupCount': this.logging_backup_count,
                'formatter': 'standard',
            },
            # Info Level - To file.
            'file_info': {
                'level': 'INFO',
                'class': this.logging_class,
                'filename': this.logging_directory.joinpath('info.log'),
                'maxBytes': this.logging_max_bytes,
                'backupCount': this.logging_backup_count,
                'formatter': 'standard',
            },
            # Query Level - To file.
            'file_query': {
                'level': 'QUERY',
                'class': this.logging_class,
                'filename': this.logging_directory.joinpath('query.log'),
                'maxBytes': this.logging_max_bytes,
                'backupCount': this.logging_backup_count,
                'formatter': 'minimal',
            },
            'file_results': {
                'level': 'RESULTS',
                'class': this.logging_class,
                'filename': this.logging_directory.joinpath('results.log'),
                'maxBytes': this.logging_max_bytes,
                'backupCount': this.logging_backup_count,
                'formatter': 'minimal',
            },
            # Warn Level - To file.
            'file_warn': {
                'level': 'WARNING',
                'class': this.logging_class,
                'filename': this.logging_directory.joinpath('warn.log'),
                'maxBytes': this.logging_max_bytes,
                'backupCount': this.logging_backup_count,
                'formatter': 'standard',
            },
            # Error Level - To file.
            'file_error': {
                'level': 'ERROR',
                'class': this.logging_class,
                'filename': this.logging_directory.joinpath('error.log'),
                'maxBytes': this.logging_max_bytes,
                'backupCount': this.logging_backup_count,
                'formatter': 'standard',
            },
        },
        'loggers': {
            # All basic logging.
            '': {
                'handlers': [
                    'console',
                    'file_debug',
                    'file_info', 'file_query', 'file_results',
                    'file_warn',
                    'file_error',
                ],
                'level': 'NOTSET',
                'propagate': False,
            }
        },
    }


def set_new_log_levels():
    """
    Function for adding new logging levels.
    """
    # Add new logging levels here.
    add_logging_level('QUERY', 25)
    add_logging_level('RESULTS', 26)

# endregion User Logging Settings


# region Logging Helper Functions

def init_logging(caller, logging_dir=None, handler_class=None, max_file_bytes=None, log_backup_count=None):
    """
    Initializes and returns an instance of the logger.
    :param caller: __name__ attribute of calling file.
    :param logging_dir: Optional override to change default logging directory.
    :param handler_class: Optional override to change default logging handler.
    :param max_file_bytes: Optional override to change default max log file size.
    :param log_backup_count: Optional override to change default max count of log files.
    :return: Instance of logger, associated with calling file's __name__.
    """
    # Define settings, if not yet created.
    if this.settings is None:

        # Check for "logging.config.custom_settings" values.
        # If exists, then a log file was already called somewhere else.
        # Assume the first logging call is closer to project entrypoint one so those values should override these ones.
        if hasattr(logging.config, 'custom_settings'):
            custom_settings = logging.config.custom_settings
            logging_dir = custom_settings.logging_directory
            handler_class = custom_settings.logging_class
            max_file_bytes = custom_settings.logging_max_bytes
            log_backup_count = custom_settings.logging_backup_count

        # Check for module variable overrides.
        if logging_dir is not None:
            # Validate input.
            if not isinstance(logging_dir, pathlib.PurePath):
                logging_dir = pathlib.Path(logging_dir).absolute()
            # Set value.
            this.logging_directory = logging_dir

        if handler_class is not None:
            # Unsure of how to validate input. However, seems to error on bad input so probably okay.
            this.logging_class = handler_class

        if max_file_bytes is not None:
            # Validate input.
            if not isinstance(max_file_bytes, int):
                raise TypeError('Expected max_file_bytes of type int. Got {0}.'.format(type(max_file_bytes)))
            # Set value.
            this.logging_max_bytes = max_file_bytes

        if log_backup_count is not None:
            # Validate input.
            if not isinstance(max_file_bytes, int):
                raise TypeError('Expected log_backup_count of type int. Got {0}.'.format(type(log_backup_count)))
            # Set value.
            this.logging_backup_count = log_backup_count

        # Create logging folder if does not exist.
        if not this.logging_directory.is_dir():
            print('Creating logging folders.')
            this.logging_directory.mkdir(parents=True, exist_ok=True)

        # Add new logging levels, as defined in method above.
        set_new_log_levels()

        # Load dictionary of settings into logger.
        this.settings = get_logging_settings()
        logging.config.dictConfig(this.settings)

        # Check if passed dictionary settings have been saved yet.
        if not hasattr(logging.config, 'custom_settings'):
            """
            Dictionary settings are not yet stored.

            Save dictionary settings so that other instances of log files can read in values.
            Helps ensure that logging for entire project will behave uniformly, such as instances where projects
            use git submodules or other forms of logic that require multiple instances of this logging file.

            In such a case, the settings in the first found instance of logging will take precedence, as it's assumed
            to be closer to the project root/entrypoint.
            """
            class CustomSettings():
                pass
            logging.config.custom_settings = CustomSettings()
            logging.config.custom_settings.logging_directory = this.logging_directory
            logging.config.custom_settings.logging_class = this.logging_class
            logging.config.custom_settings.logging_max_bytes = this.logging_max_bytes
            logging.config.custom_settings.logging_backup_count = this.logging_backup_count

    else:
        if (logging_dir is not None or
            handler_class is not None or
            max_file_bytes is not None or
            log_backup_count is not None
        ):
            raise RuntimeError(
                'One or more logging default overrides have been passed, but logging has already been initialized.'
            )

    return logging.getLogger(caller)


def add_logging_level(level_name, level_num, method_name=None):
    """
    Adds a new logging level to logger.

    Original logic from https://stackoverflow.com/a/35804945
    :param level_name: The name of new log level to create.
    :param level_num: The numerical value of new log level to create.
    :param method_name: The name of invoke method for new log level. Defaults to lowercase of level_name.
    """
    # Get method name if not provided.
    if not method_name:
        method_name = level_name.lower()

    # Check if values have already been defined in logger. Prevents accidental overriding.
    orig_log_level_name = logging.getLevelName(level_num)
    if (hasattr(logging, level_name) and
        hasattr(logging, method_name) and
        hasattr(logging.getLoggerClass(), method_name) and
        orig_log_level_name == level_name
    ):
        # Log level already set with same values. Skip setting.
        return None
    elif (hasattr(logging, level_name) or
          hasattr(logging, method_name) or
          hasattr(logging.getLoggerClass(), method_name) or
          orig_log_level_name != 'Level {0}'.format(level_num)
    ):
        # Log level partially defined with some values. Raise error.
        raise AttributeError('Level "{0}: {1}" already defined in logging module, but values do not match.'.format(
            level_num,
            level_name,
        ))

    # Methods to enable logging at new level.
    def log_for_level(self, message, *args, **kwargs):
        if self.isEnabledFor(level_num):
            self._log(level_num, message, args, **kwargs)

    def log_to_root(message, *args, **kwargs):
        logging.log(level_num, message, *args, **kwargs)

    # Set logger attributes for new level.
    logging.addLevelName(level_num, level_name)
    setattr(logging, level_name, level_num)
    setattr(logging.getLoggerClass(), method_name, log_for_level)
    setattr(logging, method_name, log_to_root)

# endregion Logging Helper Functions
