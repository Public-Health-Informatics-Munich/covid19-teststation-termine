import json
import os

import pytz


class Db:
    url = os.getenv("DB_URL") or 'postgresql://postgres:example@localhost:5432/termine'


class Settings:
    claim_timeout_min = int(os.getenv("CLAIM_TIMEOUT_MIN") or 5)
    num_display_slots = int(os.getenv("DISPLAY_SLOTS_COUNT") or 150)
    tz = pytz.timezone(os.getenv("TERMINE_TIME_ZONE") or 'Europe/Berlin')


class FrontendSettings:
    _inst = None

    @classmethod
    def by_env(cls):
        env_name = os.getenv("ENVIRONMENT") or "local"
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
