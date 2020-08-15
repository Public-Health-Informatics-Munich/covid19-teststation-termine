import json
import logging
import os
import sys

import hug

from access_control.access_control import admin_authentication
from db.directives import PeeweeContext, PeeweeSession
from db.model import FrontendConfig

FORMAT = '%(asctime)s - %(levelname)s\t%(name)s: %(message)s'
logging.basicConfig(format=FORMAT, stream=sys.stdout, level=logging.INFO)
log = logging.getLogger('appointments')
hug_api = hug.API('appointments')
hug_api.http.add_middleware(hug.middleware.LogMiddleware())


@hug.extend_api("/api")
def with_api():
    from api import api
    return [api]


@hug.extend_api("/admin_api", requires=admin_authentication)
def with_admin_api():
    from admin_api import admin_api
    return [admin_api]


@hug.static("/")
def static_dirs():
    return os.getenv("FE_STATICS_DIR") or "../termine-fe/build/",


@hug.static("/admin", requires=admin_authentication)
def admin_static_dirs():
    return os.getenv("BO_STATICS_DIR") or "../termine-bo/build/",


@hug.format.content_type('text/javascript')
def format_as_js(data: str, request=None, response=None):
    return data.encode('utf8')


@hug.get("/config.js", output=format_as_js)
def instance_config(db: PeeweeSession):
    with db.atomic():
        return f"window.config = {json.dumps(FrontendConfig.get().config)};"


@hug.get("/admin/config.js", requires=admin_authentication, output=format_as_js)
def instance_admin_config(db: PeeweeSession):
    with db.atomic():
        return f"window.config = {json.dumps(FrontendConfig.get().config)};"


@hug.get("/healthcheck")
def health_check():
    return "healthy"


@hug.get("/logout", requires=hug.authentication.basic(lambda e, f: False))
def logout():
    return 'OK'  # ä this will never authenticate


@hug.get("/logout_success", requires=hug.authentication.basic(lambda e, f: True))
def logout_success():
    return 'OK'  # todo could a redirect to / also work?


@hug.context_factory(apply_globally=True)
def create_context(*args, **kwargs):
    return PeeweeContext()


@hug.extend_api()
def with_cli():
    import cli
    return cli,


# to debug this code from intellij, create a run config for this function with interpreter arg "-f main.py"
if __name__ == '__main__':
    hug.development_runner.hug.interface.cli()
