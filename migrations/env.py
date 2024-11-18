import sys
from logging.config import fileConfig
from pathlib import Path

from alembic import context
from sqlalchemy import (
    engine_from_config,
    pool,
)

# Fix путей к пакету
MODEL_PATH = str(Path.cwd())
sys.path.append(MODEL_PATH)

from app.config import MIGRATION_URL
from app.models.request_cache import RequestCache

config = context.config

# Проверяем передан ли нам URL бд для миграций
try:
    pg_url = config.cmd_opts.pg_url
except AttributeError:
    pg_url = None

# Задаем дефолтный URL БД, если явно не передан
if not pg_url:
    config.set_main_option("sqlalchemy.url", str(MIGRATION_URL))

fileConfig(config.config_file_name)

# Таблицы, которые не нужно учитывать при генерации миграций
exclude_tables = config.get_section("alembic:exclude").get("tables", "").split(",")

target_metadata = RequestCache.metadata


def include_object(_object, name, type_, _reflected, _compare_to) -> bool:
    """
    Тут происходит логика выбора какие таблицы учитывать при миграциях
    """
    if type_ == "table" and name in exclude_tables:
        # Исключаем таблицы из "exclude_tables"
        return True
    else:
        return True


def run_migrations_offline() -> None:
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
        include_schemas=True,
        include_object=include_object,
        compare_type=True,
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """

    def process_revision_directives(_context, _revision, directives) -> None:
        if config.cmd_opts.autogenerate:
            script = directives[0]
            if script.upgrade_ops.is_empty():
                directives[:] = []

    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            include_object=include_object,
            process_revision_directives=process_revision_directives,
            include_schemas=True,
            compare_type=True,
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
