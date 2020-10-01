import sys
from datetime import datetime

import hug
from peewee import DateTimeField, IntegerField, CharField, DateField
from playhouse.migrate import PostgresqlMigrator, ProgrammingError, migrate

from config import config
from config.config import FrontendSettings
from db.directives import PeeweeSession
from db.model import Migration, db_proxy, tables, FrontendConfig

import logging
log = logging.getLogger('migration')


@hug.local()
def init_database(db: PeeweeSession):
    log.info("Initializing the Database")
    with db.atomic():
        db_proxy.create_tables(tables)
        log.info("Tables created. Setting migration level.")
        Migration.create(version=3)
        log.info("Migration level set.")


@hug.local()
def migrate_db(db: PeeweeSession):
    with db.atomic() as txs:
        migrator = PostgresqlMigrator(db)
        try:
            migration = Migration.get()
            if migration.version < 1:
                # do everything for level 1
                level_1(db, migration, migrator)
            if migration.version < 2:
                # do everything for level 1
                level_2(db, migration, migrator)
            if migration.version < 3:
                level_3(db, migration, migrator)

        except ProgrammingError:
            log.exception('Error - Migrations table not found, please run init_db first!')
            txs.rollback()
            sys.exit(1)


def level_1(db, migration, migrator):
    with db.atomic():
        booked_at_field = DateTimeField(null=True,
                                        default=lambda: datetime.now(tz=config.Settings.tz).replace(tzinfo=None))
        migrate(
            migrator.add_column('booking', 'booked_at', booked_at_field),
        )
        migration.version = 1
        migration.save()


def level_2(db, migration, migrator):
    with db.atomic():
        coupons_field = IntegerField(default=10)
        migrate(
            migrator.add_column('user', 'coupons', coupons_field),
        )
        migration.version = 2
        migration.save()


def level_3(db, migration, migrator):
    with db.atomic():
        log.info("creating table FrontendConfig...")
        db.create_tables([FrontendConfig])
        log.info("setting migration level to 3...")
        migration.version = 3
        migration.save()
        try:
            log.info("writing existing config to db...")
            config = FrontendSettings.by_env()
            FrontendConfig.create(config=config)
            log.info("wrote existing config to db.")
        except:
            log.warning("no config found for env, set values with cli command set_frontend_config.")

def level_4(db, migration, migrator):
    with db.atomic():
        street_field = CharField(null=True)
        street_number_field = CharField(null=True)
        post_code_field = CharField(null=True)
        city_field = CharField(null=True)
        birthday_field = DateField(null=True)
        reason_field = CharField(null=True)
        migrate(
            migrator.add_column('booking', 'street', street_field),
            migrator.add_column('booking', 'street_number', street_number_field),
            migrator.add_column('booking', 'post_code', post_code_field),
            migrator.add_column('booking', 'city', city_field),
            migrator.add_column('booking', 'birthday', birthday_field),
            migrator.add_column('booking', 'reason', reason_field)
        )
        migration.version = 4
        migration.save()