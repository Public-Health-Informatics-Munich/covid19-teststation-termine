import os

from peewee import PostgresqlDatabase
from playhouse.db_url import connect

from config import config
from db.model import db_proxy, tables, Migration

_instance = None


def init_database():
    _setup_db()
    with db_proxy.transaction():
        db_proxy.create_tables(tables)
        Migration.create(version=0)


def _setup_db():
    db_proxy.initialize(db_instance())


def db_instance() -> PostgresqlDatabase:
    global _instance
    if not _instance:
        _instance = connect(config.Db.url)
        _instance.connect()
    return _instance
