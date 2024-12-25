import os
from logging.config import fileConfig

from sqlalchemy import engine_from_config, pool
from alembic import context

from app.database import Base
target_metadata = Base.metadata


# 1. Alembic Config object
config = context.config

# 2. Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# 3. Import your DATABASE_URL from config.py
# Adjust the import path if your config.py is located elsewhere.
from app.config import DATABASE_URL

# 4. Set the 'sqlalchemy.url' dynamically from your config.py
config.set_main_option("sqlalchemy.url", DATABASE_URL)

# 5. Import your models' Base so Alembic can do 'autogenerate' migrations
# Example:
# from app.database import Base
# from app.models import user, block, transaction  # Or however your models are organized
# target_metadata = Base.metadata

target_metadata = None  # Or set to Base.metadata if you have a declarative base

def run_migrations_offline() -> None:
    """
    Run migrations in 'offline' mode.
    In this mode, we configure the context with just a URL
    (not an Engine). Calls to context.execute() will emit the given string to the
    script output.
    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """
    Run migrations in 'online' mode.
    In this scenario we create an Engine and associate a connection with the context.
    """
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
