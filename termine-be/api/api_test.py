import hug

import main
from conftest import get_user_login, get_change_pw_mismatch, get_change_pw_match, get_auth_header, USER


def test_change_user_password_no_match(testing_db):
    response = hug.test.patch(main, "/api/user", headers=get_user_login(), body=get_change_pw_mismatch())
    assert response.status == hug.HTTP_400


def test_change_user_password(testing_db):
    response = hug.test.patch(main, "/api/user", headers=get_user_login(), body=get_change_pw_match())
    assert response.status == hug.HTTP_200


def ignore_test_auth_user_verify_after_pw_change(testing_db):
    response = hug.test.get(main, "/config.js", headers=get_user_login())
    assert response.status == hug.HTTP_200
    response = hug.test.patch(main, "/api/user", headers=get_user_login(), body=get_change_pw_match())
    assert response.status == hug.HTTP_200
    response = hug.test.get(main, "/api/user", headers=get_user_login(), body=get_change_pw_match())
    assert response.status == hug.HTTP_401
    response = hug.test.get(main, "/config.js", headers=get_auth_header(USER, USER + "1"))
    assert response.status == hug.HTTP_200
