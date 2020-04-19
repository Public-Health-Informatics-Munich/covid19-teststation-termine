import logging

import hug
from peewee import DoesNotExist, DatabaseError

from db.directives import PeeweeContext
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


def verify_user(user_name, user_password, context: PeeweeContext):
    name = normalize_user(user_name)
    with context.db.atomic():
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
        except DatabaseError:
            log.exception("unknown error logging in: %s", user_name)
            return False


@hug.authentication.basic
def authentication(user_name, user_password, context: PeeweeContext):
    return verify_user(user_name, user_password, context)


@hug.authentication.basic
def admin_authentication(user_name, user_password, context: PeeweeContext):
    user = verify_user(user_name, user_password, context)
    if user and user.role == UserRoles.ADMIN:
        return user
    log.warning("missing admin role for: %s", user_name)
    return False

