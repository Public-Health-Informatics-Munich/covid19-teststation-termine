import json
import os

import pytz


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


class Db:
    if os.environ.get('DB_USERNAME') is not None:
        db_username = os.environ.get('DB_USERNAME')
        db_password = os.environ.get('DB_PASSWORD')
        db_port = os.environ.get('DB_PORT', '5432')
        db_host = os.environ.get('DB_HOST', 'localhost')
        db_database = os.environ.get('DB_DATABASE', 'termine')
        url = f"postgresql://{db_username}:{db_password}@{db_host}:{db_port}/{db_database}"
    else:
        url = os.environ.get(
            "DB_URL", 'postgresql://postgres:example@localhost:5432/termine')


class Settings:
    claim_timeout_min = int(os.environ.get("CLAIM_TIMEOUT_MIN", 5))
    num_display_slots = int(os.environ.get("DISPLAY_SLOTS_COUNT", 150))
    tz = pytz.timezone(os.environ.get("TERMINE_TIME_ZONE", 'Europe/Berlin'))
    disable_auth_for_booking = _bool_convert(
        os.environ.get("DISABLE_AUTH", False))
    use_ldap = _bool_convert(os.environ.get("USE_LDAP", False))


class Ldap:
    url = os.environ.get("LDAP_URL", "")
    user_dn = os.environ.get("LDAP_SYSTEM_DN", "")
    user_pw = os.environ.get("LDAP_SYSTEM_USER_PW", "")
    user_coupon_number = int(os.environ.get("LDAP_USER_COUPONS", 3))
    search_base = os.environ.get("LDAP_SEARCH_BASE", "")
    search_filter = os.environ.get("LDAP_SEARCH_FILTER", "")
    search_attribute = os.environ.get("LDAP_ATTRIBUTE", "")
    use_tls = os.environ.get("LDAP_USE_TLS", False)
    port = int(os.environ.get("LDAP_PORT", 389))
    tls_port = int(os.environ.get("LDAP_TLS_PORT", 636))


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
