import os
import sys

sys.path.insert(0, os.getcwd())

import logging

from app.core.db import get_db
from app.core.initial import init_db

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def init() -> None:
    with get_db() as session:
        init_db(session)


def main() -> None:
    logger.info("Creating initial data")
    init()
    logger.info("Initial data created")


if __name__ == "__main__":
    main()
