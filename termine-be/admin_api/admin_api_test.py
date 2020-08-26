import hug

import main
from conftest import get_user_login, get_admin_login, get_create_user_pw_mismatch, USER, get_create_user, \
    get_auth_header, get_invalid_login


def test_user_is_unauthorized(testing_db):
    response = hug.test.get(main, "/admin_api/user", headers=get_user_login())
    assert response.status == hug.HTTP_401


def test_user_is_invalid(testing_db):
    response = hug.test.get(main, "/admin_api/user", headers=get_invalid_login())
    assert response.status == hug.HTTP_401


def test_admin_is_authorized(testing_db):
    response = hug.test.get(main, "/admin_api/user", headers=get_admin_login())
    assert response.status == hug.HTTP_200


def test_create_user_password_no_match(testing_db):
    response = hug.test.put(main, "/admin_api/user", headers=get_admin_login(),
                            body=get_create_user_pw_mismatch(username="test"))
    assert response.status == hug.HTTP_400


def test_create_user_already_exists(testing_db):
    response = hug.test.put(main, "/admin_api/user", headers=get_admin_login(),
                            body=get_create_user(USER, USER + "1"))
    assert response.status == hug.HTTP_409


def ignore_test_create_user(testing_db):
    username = "test"
    password = "test123"
    response = hug.test.get(main, "/config.js", headers=get_auth_header(username, password))
    assert response.status == hug.HTTP_401
    response = hug.test.put(main, "/admin_api/user", headers=get_admin_login(),
                            body=get_create_user(username, password))
    assert response.status == hug.HTTP_200
    response = hug.test.get(main, "/config.js", headers=get_auth_header(username, password))
    assert response.status == hug.HTTP_200
    response = hug.test.get(main, "/admin_api/user", headers=get_auth_header(username, password))
    assert response.status == hug.HTTP_401
