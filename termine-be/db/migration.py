import sys
from datetime import datetime

import hug
from peewee import DateTimeField, IntegerField
from playhouse.migrate import PostgresqlMigrator, ProgrammingError, migrate

from config import config
from db.directives import PeeweeSession
from db.model import Migration, db_proxy, tables

import logging
log = logging.getLogger('migration')


@hug.local()
def init_database(db: PeeweeSession):
    log.info("Initializing the Database")
    with db.atomic():
        db_proxy.create_tables(tables)
        log.info("Tables created. Setting migration level.")
        Migration.create(version=2)
        log.info("Migration level set.")


@hug.local()
def migrate_db(db: PeeweeSession):
    with db.transaction() as txs:
        migrator = PostgresqlMigrator(db)
        try:
            migration = Migration.get()
            if migration.version < 1:
                # do everything for level 1
                level_1(db, migration, migrator)
            if migration.version < 2:
                # do everything for level 1
                level_2(db, migration, migrator)

        except ProgrammingError:
            log.exception('Error - Migrations table not found, please run init_db first!')
            txs.rollback()
            sys.exit(1)


def level_1(db, migration, migrator):
    with db.transaction():
        booked_at_field = DateTimeField(null=True,
                                        default=lambda: datetime.now(tz=config.Settings.tz).replace(tzinfo=None))
        migrate(
            migrator.add_column('booking', 'booked_at', booked_at_field),
        )
        migration.version = 1
        migration.save()


def level_2(db, migration, migrator):
    with db.transaction():
        coupons_field = IntegerField(default=10)
        migrate(
            migrator.add_column('user', 'coupons', coupons_field),
        )
        migration.version = 2
        migration.save()
