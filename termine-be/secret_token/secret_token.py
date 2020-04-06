import hashlib
import random
import string

from config import config


def get_secret_token(length: int) -> str:
    letters = 'ABCDEFGHJKLMNPQRSTUVWXYZ'
    return random.choice(letters) + '-' + ''.join([random.choice(string.digits) for _ in range(length - 1)])


def get_random_string(length: int) -> str:
    return ''.join([random.choice(string.ascii_letters) for _ in range(length)])


def hash_secret(secret: str) -> str:
    return hashlib.sha512(secret.encode('utf8')).hexdigest()


def hash_pw(name, salt, user_password):
    return hash_secret(name + salt + user_password + config.seed)
