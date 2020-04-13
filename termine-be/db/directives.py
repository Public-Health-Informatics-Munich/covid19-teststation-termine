"""Defines how connections with databases via peewee will be handled"""
import logging

import hug
from peewee import Database
from playhouse.db_url import connect

from config import config
from .model import db_proxy

log = logging.getLogger("db.directives")


class PeeweeContext:
    _cls_db = None
    _testing = False

    @classmethod
    def set_testing(cls):
        cls._testing = True

    @classmethod
    def get_connection(cls, testing):
        url = "sqlite:///:memory:" if testing else config.Db.url
        log.debug("connecting db, %s testing: %s", cls, testing)
        return connect(url)

    @classmethod
    def _static_db(cls, testing):
        if testing:
            cls._cls_db = cls._cls_db or cls.get_connection(testing)
            return cls._cls_db
        else:
            return cls.get_connection(False)

    def __init__(self):
        log.debug("init PeeweeContext, %s", self)
        db_proxy.initialize(self._static_db(PeeweeContext._testing))

    @property
    def db(self) -> Database:
        return self._static_db(PeeweeContext._testing)

    def cleanup(self, exception=None):
        log.debug("cleaning up PeeweeContext")
        if exception:
            log.exception("errror in PeeweeContext: ", exception)


@hug.directive(apply_globally=True)
class PeeweeSession:
    def __new__(cls, context: PeeweeContext, *args, **kwargs):
        log.debug('Entering PeeweeSession')
        return context.db
