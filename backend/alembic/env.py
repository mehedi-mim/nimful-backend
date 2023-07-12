import os
from logging.config import fileConfig

from alembic import context
from sqlalchemy import engine_from_config
from sqlalchemy import pool

from db import Base

config = context.config

fileConfig(config.config_file_name)

target_metadata = Base.metadata


def include_object(object, name, type_, reflected, compare_to):
    excluded_tables = ['default_partition']

    # Generate excluded tables with pattern 'livestream_events_p*'
    # supoorts up to 100
    excluded_tables.extend([f'livestream_events_p{i}' for i in range(1, 101)])

    should_exclude = name in excluded_tables

    if compare_to is None:
        index_belongs_to_excluded_table = False
    else:
        index_belongs_to_excluded_table = compare_to in excluded_tables

    table_config = (type_ == "table" and should_exclude)
    index_config = (type_ == "index" and index_belongs_to_excluded_table)

    return not any([
        table_config,
        index_config
    ])


def get_url():
    url = os.getenv("DATABASE_URL_ALEMBIC")
    return url


def run_migrations_offline():
    url = get_url()
    context.configure(
        url=url, target_metadata=target_metadata, literal_binds=True,
        compare_type=True
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    configuration = config.get_section(config.config_ini_section)
    configuration["sqlalchemy.url"] = get_url()
    connectable = engine_from_config(
        configuration,
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            include_object=include_object
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
