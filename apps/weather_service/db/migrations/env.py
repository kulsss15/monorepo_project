import sys
from pathlib import Path
from logging.config import fileConfig
from alembic import context
from sqlalchemy import engine_from_config, pool

# Add the root directory to PYTHONPATH
sys.path.append(str(Path(__file__).resolve().parents[3]))

# Import settings
from apps.weather_service.core.config import settings
from apps.weather_service.db.models import Base  # Adjust to your models

# Load Alembic config
config = context.config
fileConfig(config.config_file_name)

# Set up the database URL dynamically
config.set_main_option("sqlalchemy.url", settings.DATABASE_URL)

# Metadata for Alembic
target_metadata = Base.metadata

def run_migrations_online():
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )
    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)
        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    raise NotImplementedError("Offline mode is not implemented.")
else:
    run_migrations_online()
