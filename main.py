
# System Imports.
from abc import ABC, abstractmethod

# User Imports.
from src.connectors.core import AbstractDbConnector
from src.logging import init_logging


# Import logger.
logger = init_logging(__name__)


def main():
    connector = AbstractDbConnector(debug=True)


if __name__ == '__main__':
    logger.info('Initializing program.')
    main()
    logger.info('Terminating program.')
