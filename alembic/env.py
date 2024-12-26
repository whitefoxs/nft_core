# alembic/env.py

import os
from logging.config import fileConfig

from sqlalchemy import engine_from_config, pool
from alembic import context

from app.models.block import Block
from app.models.transaction import Transaction

# 1. Alembic config
config = context.config

# 2. Logging
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# 3. Import DB stuff
from app.config import DATABASE_URL
from app.database import Base
# Import the models so Alembic sees them
from app.models.user import User
from app.models.user_kyc import UserKyc

# 4. Override the sqlalchemy.url with our DATABASE_URL
config.set_main_option("sqlalchemy.url", DATABASE_URL)

# 5. Target metadata
target_metadata = Base.metadata


def run_migrations_offline() -> None:
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
