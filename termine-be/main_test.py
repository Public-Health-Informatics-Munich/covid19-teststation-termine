import hug

import main


def test_test():
    # assert that the tests run
    assert True


def test_instance_config():
    response = hug.test.get(main, "/config.js")
    assert response.status == hug.HTTP_401
