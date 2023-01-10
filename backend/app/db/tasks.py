import logging

from fastapi import FastAPI
from sqlalchemy import create_engine

from app._config import db_string

logger = logging.getLogger(__name__)


async def check_connect_to_db(app: FastAPI) -> None:
    try:
        database = create_engine(db_string)
        database.connect()

    except Exception as e:
        logger.warn("--- DATABASE CONNECTION ERR ---")
        logger.warn(e)
