"""A module providing database access."""

import asyncio

import databases
import sqlalchemy
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.exc import OperationalError, DatabaseError
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.mutable import MutableList
from asyncpg.exceptions import (    # type: ignore
    CannotConnectNowError,
    ConnectionDoesNotExistError,
)

from src.config import config

metadata = sqlalchemy.MetaData()

league_table = sqlalchemy.Table(
    "leagues",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("name", sqlalchemy.String),
    sqlalchemy.Column("city", sqlalchemy.String),
    sqlalchemy.Column("sport_type", sqlalchemy.String),
    sqlalchemy.Column("is_private", sqlalchemy.Boolean, default=False),
    sqlalchemy.Column("owner_id", sqlalchemy.Integer, sqlalchemy.ForeignKey("users.id"), nullable=False),
    sqlalchemy.Column("status", sqlalchemy.String, default="active"),
)

team_table = sqlalchemy.Table(
    "teams",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("name", sqlalchemy.String),
    sqlalchemy.Column(
        "league_id",
        sqlalchemy.ForeignKey("leagues.id"),
        nullable=False,
    ),
    sqlalchemy.Column(
        "captain_id",
        sqlalchemy.Integer,
        sqlalchemy.ForeignKey("users.id"),
        nullable=False,
    ),
)

match_table = sqlalchemy.Table(
    "matches",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column(
        "league_id",
        sqlalchemy.ForeignKey("leagues.id"),
        nullable=False,
    ),
    sqlalchemy.Column(
        "home_team_id",
        sqlalchemy.ForeignKey("teams.id"),
        nullable=False,
    ),
    sqlalchemy.Column(
        "away_team_id",
        sqlalchemy.ForeignKey("teams.id"),
        nullable=False,
    ),
    sqlalchemy.Column("home_score", sqlalchemy.Integer, nullable=True),
    sqlalchemy.Column("away_score", sqlalchemy.Integer, nullable=True),
    sqlalchemy.Column("date", sqlalchemy.String),
    sqlalchemy.Column("status", sqlalchemy.String, default="scheduled"),
    sqlalchemy.Column(
        "submitted_by",
        sqlalchemy.Integer,
        sqlalchemy.ForeignKey("users.id"),
        nullable=True,
    ),
)

invitation_table = sqlalchemy.Table(
    "invitations",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column(
        "league_id",
        sqlalchemy.ForeignKey("leagues.id"),
        nullable=False,
    ),
    sqlalchemy.Column("token", sqlalchemy.String, nullable=False, unique=True),
    sqlalchemy.Column("expires_at", sqlalchemy.DateTime, nullable=False),
    sqlalchemy.Column(
        "used_by",
        sqlalchemy.Integer,
        sqlalchemy.ForeignKey("users.id"),
        nullable=True,
    ),
)

user_table = sqlalchemy.Table(
    "users",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("email", sqlalchemy.String, unique=True),
    sqlalchemy.Column("password", sqlalchemy.String),
)

db_uri = (
    f"postgresql+asyncpg://{config.DB_USER}:{config.DB_PASSWORD}"
    f"@{config.DB_HOST}/{config.DB_NAME}"
)

engine = create_async_engine(
    db_uri,
    echo=True,
    future=True,
    pool_pre_ping=True,
)

database = databases.Database(
    db_uri,
    force_rollback=False,
)


async def init_db(retries: int = 5, delay: int = 5) -> None:
    """Function initializing the DB.

    Args:
        retries (int, optional): Number of retries of connect to DB.
            Defaults to 5.
        delay (int, optional): Delay of connect do DB. Defaults to 2.
    """
    for attempt in range(retries):
        try:
            async with engine.begin() as conn:
                await conn.run_sync(metadata.create_all)
            return
        except (
            OperationalError,
            DatabaseError,
            CannotConnectNowError,
            ConnectionDoesNotExistError,
        ) as e:
            print(f"Attempt {attempt + 1} failed: {e}")
            await asyncio.sleep(delay)

    raise ConnectionError("Could not connect to DB after several retries.")
