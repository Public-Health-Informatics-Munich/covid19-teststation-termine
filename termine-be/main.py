import logging
import os
import sys

import hug

import cli
from access_control.access_control import authentication, admin_authentication
from admin_api import admin_api
from api import api
from config.config import FrontendSettings
from db.directives import PeeweeContext

FORMAT = '%(asctime)s - %(levelname)s\t%(name)s: %(message)s'
logging.basicConfig(format=FORMAT, stream=sys.stdout, level=logging.INFO)
log = logging.getLogger('termine')

hug_api = hug.API(__name__)
hug_api.http.add_middleware(hug.middleware.LogMiddleware())


@hug.extend_api("/api", requires=authentication)
def with_api():
    return [api]


@hug.extend_api("/admin_api", requires=admin_authentication)
def with_admin_api():
    return [admin_api]


@hug.static("/", requires=authentication)
def static_dirs():
    return os.getenv("FE_STATICS_DIR") or "../termine-fe/build/",


@hug.static("/admin", requires=admin_authentication)
def admin_static_dirs():
    return os.getenv("BO_STATICS_DIR") or "../termine-bo/build/",


@hug.format.content_type('text/javascript')
def format_as_js(data: str, request=None, response=None):
    return data.encode('utf8')


@hug.get("/config.js", requires=authentication, output=format_as_js)
def instance_config():
    return 'window.config = ' + FrontendSettings.json_by_env() + ';'


@hug.get("/admin/config.js", requires=admin_authentication, output=format_as_js)
def instance_admin_config():
    return 'window.config = ' + FrontendSettings.json_by_env() + ';'


@hug.get("/healthcheck")
def health_check():
    return "healthy"


@hug.get("/logout", requires=hug.authentication.basic(lambda e, f: False))
def logout():
    return 'OK'  # ä this will never authenticate


@hug.get("/logout_success", requires=hug.authentication.basic(lambda e, f: True))
def logout_success():
    return 'Ok'  # todo could a redirect to / also work?


@hug.extend_api(sub_command="db")
def with_cli():
    return cli,


@hug.context_factory()
def create_context(*args, **kwargs):
    return PeeweeContext()


# to debug this code from intellij, create a run config for this function with interpreter arg "-f main.py"
if __name__ == '__main__':
    hug.development_runner.hug.interface.cli()
