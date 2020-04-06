import logging

import hug
from peewee import DoesNotExist

from db.db import _setup_db, db_instance
from db.model import User
from secret_token.secret_token import hash_pw

log = logging.getLogger('auth')


class UserRoles:
    ADMIN = 'admin'
    USER = 'doctor'

    @staticmethod
    def user_roles():
        return [UserRoles.ADMIN, UserRoles.USER]


def normalize_user(user_name):
    return user_name.lower()


def _verify_user(user_name, user_password):
    _setup_db()
    name = normalize_user(user_name)
    with db_instance().transaction():
        try:
            user = User.get(User.user_name == name)
            salt = user.salt
            hashed = hash_pw(name, salt, user_password)
            if hashed == user.password:
                return user
            log.warning("invalid credentials for user: %s", user_name)
            return False
        except DoesNotExist:
            log.warning("user not found: %s", user_name)
            return False
        except:
            log.warning("unknown error logging in: %s", user_name)
            return False


def _verify_admin(user_name, user_password):
    user = _verify_user(user_name, user_password)
    if user.role == UserRoles.ADMIN:
        return user
    log.warning("missing admin role for: %s", user_name)
    return False


def verify():
    """Returns a simple verification callback that simply verifies that the users and password match with the db"""
    return _verify_user


def verify_admin():
    """Returns a callback that verifies that the users and password match with the db and the role is UserRoles.ADMIN"""
    return _verify_admin


authentication = hug.authentication.basic(verify())
admin_authentication = hug.authentication.basic(verify_admin())
