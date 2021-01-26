import logging

import hug
import base64
import binascii
from ldap3 import Server, Connection, ALL
from peewee import DoesNotExist, DatabaseError
from falcon import HTTPUnauthorized

from db.directives import PeeweeContext
from db.model import User
from config import config
from secret_token.secret_token import hash_pw

log = logging.getLogger('auth')


class UserRoles:
    ADMIN = 'admin'
    USER = 'doctor'
    ANON = 'anonymous'

    @staticmethod
    def user_roles():
        return [UserRoles.ADMIN, UserRoles.USER, UserRoles.ANON]


def normalize_user(user_name):
    return user_name.lower()


def verify_user(user_name, user_password, context: PeeweeContext):
    name = normalize_user(user_name)
    if config.Settings.use_ldap:
        server = Server(config.Ldap.url, port=3389, get_info=ALL)
        connection = Connection(
            server, 'uid=termine,ou=Application,dc=example,dc=com', 'appsecret')
        result = connection.bind()
        log.info(result)
        log.info(connection)
        return result
    else:
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
                log.warning("user not found: %s", user_name)
                return False
            except DatabaseError:
                log.exception("unknown error logging in: %s", user_name)
                return False


def get_or_create_anon_user(context: PeeweeContext):
    name = "unregistered_user"
    with context.db.atomic():
        try:
            user = User.get(User.user_name == name)
            return user
        except DoesNotExist:
            user = User.create(user_name=name, role=UserRoles.ANON,
                               salt="", password="", coupons=4)
            user.save()
            return user


@hug.authentication.authenticator
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


@basic
def switchable_authentication(user_name, user_password, context: PeeweeContext):
    return verify_user(user_name, user_password, context)


@hug.authentication.basic
def authentication(user_name, user_password, context: PeeweeContext):
    user = verify_user(user_name, user_password, context)
    if user and user.role == UserRoles.ANON:
        return False
    return user


@hug.authentication.basic
def admin_authentication(user_name, user_password, context: PeeweeContext):
    user = verify_user(user_name, user_password, context)
    if user and user.role == UserRoles.ADMIN:
        return user
    log.warning("missing admin role for: %s", user_name)
    return False
