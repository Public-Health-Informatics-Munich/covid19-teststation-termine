"""Defines how connections with databases via peewee will be handled"""
import hug
from peewee import Database
from playhouse.db_url import connect

from config import config
from .model import db_proxy, tables, Migration
import logging

log = logging.getLogger("db.directives")


class PeeweeContext:
    def __init__(self):
        self._db = connect(config.Db.url)
        db_proxy.initialize(self._db)

    @property
    def db(self) -> Database:
        return self._db

    def cleanup(self, exception=None):
        log.debug("cleaning up PeeweeContext")
        if exception:
            log.exception("errror in PeeweeContext: ", exception)


@hug.directive()
class PeeweeSession:
    def __new__(cls, *args, context: PeeweeContext = None, **kwargs):
        log.debug('Entering PeeweeSession')
        return context.db


@hug.local()
def init_database(context: PeeweeContext):
    with context.db.atomic():
        db_proxy.create_tables(tables)
        Migration.create(version=2)
