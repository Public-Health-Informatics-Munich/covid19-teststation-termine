import hug

import main
from conftest import get_user_login, get_change_pw_mismatch, get_change_pw_match


def test_change_user_password_no_match(testing_db):
    response = hug.test.patch(
        main, "/api/user", headers=get_user_login(), body=get_change_pw_mismatch())
    assert response.status == hug.HTTP_400


def test_change_user_password(testing_db):
    response = hug.test.patch(
        main, "/api/user", headers=get_user_login(), body=get_change_pw_match())
    assert response.status == hug.HTTP_200
