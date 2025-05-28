import os
import sys
from logging.config import fileConfig

from sqlalchemy import engine_from_config, pool
from alembic import context

sys.path.append(os.path.abspath("."))

from app.database.connection import DATABASE_URL, engine
from app.models.base import SQLModel

# QLModel
from app.models.user import User
from app.models.envent import Event

target_metadata = SQLModel.metadata

def run_migrations_offline():
    """Run migrations in 'offline' mode.
    ...
    """
    context.configure(
        url=DATABASE_URL,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    """Run migrations in 'online' mode.
    ...
    """
    with engine.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
