import os
import sys
import pathlib

from logging.config import fileConfig

from sqlalchemy import pool, engine_from_config, create_engine

from alembic import context

from psycopg2 import DatabaseError

# we're appending the app directory to our path here so that we can import config easily
sys.path.append(str(pathlib.Path(__file__).resolve().parents[2]))

from core.config.config import DATABASE_URL, POSTGRES_DB # noqa

from model import Dna, Statistics
from db import Base

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
fileConfig(config.config_file_name)

# add your model's MetaData object here
# for 'autogenerate' support
# from myapp import mymodel
# target_metadata = mymodel.Base.metadata
target_metadata = Base.metadata

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.


def run_migrations_offline():
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    if os.environ.get("TESTING"):
        raise DatabaseError("Running testing migrations offline currently not permitted.")

    url = DATABASE_URL
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    DB_URL = f'{DATABASE_URL}_test' if os.environ.get('TESTING') else DATABASE_URL

    if os.environ.get("TESTING"):
        # connect to primary db
        engine = create_engine(DATABASE_URL, isolation_level="AUTOCOMMIT")
        # drop testing db if it exists use FORCE to end with all connections are stuck or still alive and create a fresh one
        with engine.connect() as default_conn:
            default_conn.execute(f"DROP DATABASE IF EXISTS {POSTGRES_DB}_test WITH (FORCE)")
            default_conn.execute(f"CREATE DATABASE {POSTGRES_DB}_test")

    config.set_main_option("sqlalchemy.url", DB_URL)
    
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
