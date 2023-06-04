from logging.config import fileConfig

from pydantic import PostgresDsn
from sqlalchemy import create_engine, engine_from_config, pool

from alembic import context
from src.config import db_config
from src.db.base_class import Base

# autogenerate checks the models in this import to see if they have changed
from src.models import *  # isort:skip # noqa

target_metadata = [Base.metadata]

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
fileConfig(config.config_file_name)

config.set_main_option("sqlalchemy.url", db_config.DATABASE_URL)


def run_migrations_offline():
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        compare_type=True,
    )

    with context.begin_transaction():
        context.run_migrations()


def check_and_create_db():
    db_url = PostgresDsn.build(
        scheme="postgresql+psycopg2",
        user=db_config.POSTGRES_USER,
        password=db_config.POSTGRES_PASSWORD,
        host=db_config.POSTGRES_SERVER,
        path=f"/postgres",
    )
    engine = create_engine(db_url)
    connection = None
    try:
        connection = engine.connect()
        result = connection.execute(
            f"SELECT 1 FROM pg_database WHERE datname = '{db_config.POSTGRES_DB}'"
        )
        exists = result.fetchone()
        if not exists:
            connection.execution_options(isolation_level="AUTOCOMMIT").execute(
                f"CREATE DATABASE {db_config.POSTGRES_DB}"
            )
    finally:
        if connection:
            connection.close()


def run_migrations_online():
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    check_and_create_db()
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            compare_type=True,
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
