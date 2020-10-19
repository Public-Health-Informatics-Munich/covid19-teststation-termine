import sys
from datetime import datetime

import hug
import re
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
        Migration.create(version=5)
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
            if migration.version < 4:
                level_4(db, migration, migrator)
            if migration.version < 5:
                level_5(db, migration)


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

def level_5(db, migration):
    left_part_coupons = '<span class="hintLabel">Um mehr Termine vergeben zu können wenden Sie sich an '
    left_part_appointment = '<span class=\"hintLabel\">Kontaktieren Sie '
    rigth_part = '</span>'
    mail_extract = 'href="mailto:([a-zA-Z0-9!#$%&\'*+-/=?^_`{|}~.@]*)"'
    with db.atomic():
        try:
            frontend_config = FrontendConfig.get()

            contact_info_coupons = frontend_config.config['contactInfoCoupons']
            contact_info_appointment = frontend_config.config['contactInfoAppointment']
            contact_info_appointment = contact_info_appointment.lstrip(left_part_appointment).rstrip(rigth_part)
            contact_info_coupons = contact_info_coupons.lstrip(left_part_coupons).rstrip(rigth_part)
            if contact_info_coupons.find('@') >= 0:
                contact_info_coupons = re.findall(mail_extract, contact_info_coupons)[0]
            if contact_info_appointment.find('@') >= 0:
                contact_info_appointment = re.findall(mail_extract, contact_info_appointment)[0]
            frontend_config.config['contactInfoCoupons'] = contact_info_coupons
            frontend_config.config['contactInfoAppointment'] = contact_info_appointment
            frontend_config.save()
            migration.version = 5
            migration.save()
        except IndexError:
            log.info("No frontendconfig stored. No row migration needed")
