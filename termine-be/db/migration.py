import sys
from datetime import datetime

from peewee import DateTimeField, IntegerField
from playhouse.migrate import PostgresqlMigrator, ProgrammingError, migrate

from config import config
from db.db import _setup_db, db_instance
from db.model import Migration


def migrate_db():
    _setup_db()
    database = db_instance()
    migrator = PostgresqlMigrator(database)
    try:
        migration = Migration.get()
        if migration.version < 1:
            # do everything for level 1
            level_1(database, migration, migrator)
        if migration.version < 2:
            # do everything for level 1
            level_2(database, migration, migrator)

    except ProgrammingError as e:
        print(e)
        print('Error - Migrations table not found, please run init_db first!')
        sys.exit(1)


def level_1(database, migration, migrator):
    with database.transaction():
        booked_at_field = DateTimeField(null=True,
                                        default=lambda: datetime.now(tz=config.Settings.tz).replace(tzinfo=None))
        migrate(
            migrator.add_column('booking', 'booked_at', booked_at_field),
        )
        migration.version = 1
        migration.save()


def level_2(database, migration, migrator):
    with database.transaction():
        coupons_field = IntegerField(default=10)
        migrate(
            migrator.add_column('user', 'coupons', coupons_field),
        )
        migration.version = 2
        migration.save()
