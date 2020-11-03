import hug

import main
from conftest import get_user_login, get_invalid_login


def test_test():
    # make sure the tests run
    assert True


def test_auth_no_verify(testing_db):
    response = hug.test.get(main, "/api/booked", headers=get_invalid_login())
    assert response.status == hug.HTTP_401


def test_auth_user_verify(testing_db):
    response = hug.test.get(main, "/config.js", headers=get_user_login())
    assert response.status == hug.HTTP_200
