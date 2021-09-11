import asyncio
import logging
from pathlib import Path
from typing import List

import asyncpg

from bot.constants import Client


logger = logging.getLogger(__name__)


async def init_db():
    """Connect to database and create initial tables."""
    conn: asyncpg.Connection = await asyncpg.connect(Client.database_url)

    tables = Path("postgres", "tables")

    logger.info("Creating tables.")

    for table_file in tables.iterdir():
        await conn.execute(table_file.read_text())

    return conn


async def db_execute(conn: asyncpg.Connection, sql_statement: str, *args) -> str:
    """Execute SQL statement."""
    logger.info(f"Executing SQL: {sql_statement}")
    logger.info(f"with args: {args}")
    status = await conn.execute(sql_statement, *args)
    logger.info(f"DB execute {status =}")
    return status


async def db_fetch(conn: asyncpg.Connection, sql_statement: str, *args) -> List[asyncpg.Record]:
    """Fetch from db.."""
    logger.info(f"Fetching from DB: {sql_statement}")
    logger.info(f"with args: {args}")
    result = await conn.fetch(
        sql_statement,
        *args,
    )
    logger.info(f"DB fetch {result =}")
    return result
    
