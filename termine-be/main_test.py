from base64 import b64encode

import hug

import main
from db.directives import PeeweeContext

PeeweeContext.set_testing()


def get_basic_auth(user, pw):
    return "Basic " + b64encode(f"{user}:{pw}".encode("utf-8")).decode('utf-8')


def test_test():
    # make sure the tests run
    assert True


def test_db_connection():
    # make sure the tests connect to the testing db
    hug.test.cli("init_db", for_real=True, module='main')
    response = hug.test.get(main, "/config.js")
    assert response.status == hug.HTTP_401
    hug.test.cli("add_user", "test", password='test', module='main')
    response = hug.test.get(main, "/config.js",
                            headers={"Authorization": get_basic_auth("test", "test")})
    assert response.status == hug.HTTP_200
