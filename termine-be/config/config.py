import json
import os
import marshmallow as ma
import typing

import pytz


class Db:
    url = os.environ.get("DB_URL", 'postgresql://postgres:example@localhost:5432/termine')


class Settings:
    _int_ma = ma.fields.Int(missing=typing.Any)
    _bool_ma = ma.fields.Bool(missing=typing.Any)
    claim_timeout_min = _int_ma.deserialize(os.environ.get("CLAIM_TIMEOUT_MIN", 5))
    num_display_slots = _int_ma.deserialize(os.environ.get("DISPLAY_SLOTS_COUNT", 150))
    tz = pytz.timezone(os.environ.get("TERMINE_TIME_ZONE", 'Europe/Berlin'))
    disable_auth_for_booking = _bool_ma.deserialize(os.environ.get("DISABLE_AUTH", False))


class FrontendSettings:
    _inst = None

    @classmethod
    def by_env(cls):
        env_name = os.environ.get("ENVIRONMENT", "local")
        with open(os.path.join("config", 'by_env', f'{env_name}.json')) as file:
            frontend_conf = json.load(file)
            return frontend_conf

    @classmethod
    def instance_by_env(cls):
        if not cls._inst:
            cls._inst = cls.by_env()
        return cls._inst

    @classmethod
    def json_by_env(cls):
        return json.dumps(cls.instance_by_env())


seed = os.getenv("PASSWORD_HASH_SEED_DO_NOT_CHANGE") or 'Wir sind SEEED'
