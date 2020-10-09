import json
import os

import pytz


class Db:
    url = os.environ.get("DB_URL", 'postgresql://postgres:example@localhost:5432/termine')


class Settings:
    @staticmethod
    def _bool_convert(value):
        truthy = {"t", "true", "on", "y", "yes", "1", 1, 1.0, True}
        falsy = {"f", "false", "off", "n", "no", "0", 0, 0.0, False}
        if isinstance(value, str):
            value = value.lower()
        if value in truthy:
            return True
        if value in falsy:
            return False
        return bool(value)

    claim_timeout_min = int(os.environ.get("CLAIM_TIMEOUT_MIN", 5))
    num_display_slots = int(os.environ.get("DISPLAY_SLOTS_COUNT", 150))
    tz = pytz.timezone(os.environ.get("TERMINE_TIME_ZONE", 'Europe/Berlin'))
    disable_auth_for_booking = _bool_convert(os.environ.get("DISABLE_AUTH", False))


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


seed = os.environ.get("PASSWORD_HASH_SEED_DO_NOT_CHANGE", 'Wir sind SEEED')
