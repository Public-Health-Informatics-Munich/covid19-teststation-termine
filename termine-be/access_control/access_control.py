import logging
import jwt
import hug
import base64
import binascii
from ldap3 import SIMPLE, Server, Connection, ALL
from peewee import DoesNotExist, DatabaseError
from falcon import HTTPUnauthorized

from db.directives import PeeweeContext, PeeweeSession
from db.model import User
from config import config
from secret_token.secret_token import hash_pw

log = logging.getLogger('auth')


def token_verify(token, context: PeeweeContext):
    secret = config.Settings.jwt_key
    try:
        user_object = jwt.decode(token, secret, algorithms=["HS256"])
        return get_user(user_object['user'], context)
    except jwt.DecodeError as error:
        log.warning("decodeError {}".format(error))
        return False


token_key_authentication = hug.authentication.token(token_verify)


class UserRoles:
    ADMIN = 'admin'
    USER = 'doctor'
    ANON = 'anonymous'

    @staticmethod
    def user_roles():
        return [UserRoles.ADMIN, UserRoles.USER, UserRoles.ANON]


def normalize_user(user_name):
    return user_name.lower()


def get_user(user_name: str, context: PeeweeContext):
    with context.db.atomic():
        try:
            return User.get(User.user_name == user_name)
        except DoesNotExist:
            log.warning("user not found: %s", user_name)
            return False
        except DatabaseError:
            log.exception("unknown error logging in: %s", user_name)
            return False


def verify_user(user_name, user_password, context: PeeweeContext):
    name = normalize_user(user_name)
    with context.db.atomic():
        try:
            user = User.get(User.user_name == name)
            if user.role == UserRoles.ANON:
                return user
            salt = user.salt
            hashed = hash_pw(name, salt, user_password)
            if hashed == user.password:
                return user
            log.warning("invalid credentials for user: %s", user_name)
            return False
        except DoesNotExist:
            if config.Settings.use_ldap:
                return search_ldap_user(user_name, user_password, context)
            else:
                log.warning("user not found: %s", user_name)
                return False
        except DatabaseError:
            log.exception("unknown error logging in: %s", user_name)
            return False


def search_ldap_user(user_name: str, user_password: str, context: PeeweeContext):
    url = config.Ldap.url
    sys_user = config.Ldap.user_dn
    sys_pw = config.Ldap.user_pw
    base = config.Ldap.search_base
    filter = config.Ldap.search_filter
    attribute = config.Ldap.search_attribute
    if "" in [url, sys_user, sys_pw, base, filter, attribute]:
        log.error(
            "ENV variables for LDAP not set. You'll need to define LDAP_URL, LDAP_SYSTEM_DN, LDAP_SYSTEM_USER_PW, LDAP_SEARCH_BASE, LDAP_SEARCH_FILTER, LDAP_ATTRIBUTE")
        return False

    with_tls = config.Ldap.use_tls
    port = config.Ldap.tls_port if with_tls else config.Ldap.port
    server = Server(url, port=port, use_ssl=with_tls,
                    get_info=ALL)

    # Connects the system user
    connection = Connection(
        server, sys_user, sys_pw)
    result = connection.bind()
    if with_tls:
        connection.start_tls()
    if result:
        # searches for the user about to log in in the ldap server
        connection.search(base, filter.format(
            user_name), attributes=[attribute])
        # if exactly one was found, tries to log this one in
        if len(connection.entries) == 1:
            userConnection = Connection(
                server, user=connection.entries[0].entry_dn, password=user_password, authentication=SIMPLE)
            isValid = userConnection.bind()
            if isValid:
                # creates a user if not existing yet, in order to track coupon numbers per ldap user
                return get_or_create_auto_user(context.db, UserRoles.USER, f'ldap-{user_name}')
    log.warning(f"Didn't find an ldap user for uid {user_name}")
    return False


def get_or_create_anon_user(context: PeeweeContext):
    name = "unregistered_user"
    return get_or_create_auto_user(context.db, UserRoles.ANON, name)


def get_or_create_auto_user(db: PeeweeSession, role: str, name: str):
    coupons = 4 if (
        role == UserRoles.ANON) else config.Ldap.user_coupon_number if role == UserRoles.USER else 1
    with db.atomic():
        try:
            user = User.get(User.user_name == name)
            return user
        except DoesNotExist:
            user = User.create(user_name=name, role=role,
                               salt="", password="", coupons=coupons)
            user.save()
            return user


@ hug.authentication.authenticator
def basic(request, response, own_verify_user, realm="simple", context=None, **kwargs):
    """Basic HTTP Authentication"""
    http_auth = request.auth
    response.set_header("WWW-Authenticate", "Basic")

    if http_auth is None:
        if config.Settings.disable_auth_for_booking:
            user = get_or_create_anon_user(context)
            return user
        return

    if isinstance(http_auth, bytes):
        http_auth = http_auth.decode("utf8")
    try:
        auth_type, user_and_key = http_auth.split(" ", 1)
    except ValueError:
        raise HTTPUnauthorized(
            "Authentication Error",
            "Authentication header is improperly formed",
            challenges=('Basic realm="{}"'.format(realm),),
        )
    if auth_type.lower() == "basic":
        try:
            user_id, key = (
                base64.decodebytes(bytes(user_and_key.strip(), "utf8")).decode(
                    "utf8").split(":", 1)
            )
            user = own_verify_user(user_id, key, context)
            if user:
                response.set_header("WWW-Authenticate", "")
                return user
        except (binascii.Error, ValueError):
            raise HTTPUnauthorized(
                "Authentication Error",
                "Unable to determine user and password with provided encoding",
                challenges=('Basic realm="{}"'.format(realm),),
            )
    return False


@ basic
def switchable_authentication(user_name, user_password, context: PeeweeContext):
    return verify_user(user_name, user_password, context)


@ hug.authentication.basic
def authentication(user_name, user_password, context: PeeweeContext):
    user = verify_user(user_name, user_password, context)
    if user and user.role == UserRoles.ANON:
        return False
    return user


@ hug.authentication.basic
def admin_authentication(user_name, user_password, context: PeeweeContext):
    user = verify_user(user_name, user_password, context)
    if user and user.role == UserRoles.ADMIN:
        return user
    log.warning("missing admin role for: %s", user_name)
    return False
