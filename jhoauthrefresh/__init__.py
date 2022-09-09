import os
import json

from jupyter_server.base.handlers import JupyterHandler
from jupyter_server.serverapp import ServerApp
import tornado
from tornado import web
from tornado.ioloop import IOLoop
from tornado.ioloop import PeriodicCallback
from tornado.httpclient import AsyncHTTPClient, HTTPRequest
from notebook.utils import url_path_join

from .config import JHOauthRefreshConfig


class TokenHandler(JupyterHandler):
    @tornado.web.authenticated
    async def get(self):
        config = self.settings["jhoauthrefresh"]
        self.write(os.getenv(config.oauth_token_env_var))


def setup_handlers(web_app, endpoint):
    web_app.add_handlers(
        ".*", [(url_path_join(web_app.settings["base_url"], endpoint), TokenHandler,)],
    )


async def fetch_new_token(token, url):
    req = HTTPRequest(url, headers={"Authorization": "token %s" % token})

    client = AsyncHTTPClient()
    resp = await client.fetch(req)

    resp_json = json.loads(resp.body.decode("utf8", "replace"))
    return resp_json


async def update(config):
    jhub_api_token = os.getenv(config.jupyterhub_token_env_var)
    tokens = await fetch_new_token(jhub_api_token, config.new_token_url)
    os.environ[config.oauth_token_env_var] = tokens["access_token"]


def _jupyter_server_extension_points():
    return [{"module": "jhoauthrefresh",}]


def _load_jupyter_server_extension(serverapp: ServerApp):
    """
    This function is called when the extension is loaded.
    """
    config = JHOauthRefreshConfig(config=serverapp.config)
    serverapp.web_app.settings["jhoauthrefresh"] = config
    setup_handlers(serverapp.web_app, config.extension_endpoint)

    # update once at the start to handle the case where the server is
    # being started so long after the login that the token itself has
    # expired so we need to refresh it straight away
    loop = IOLoop.current()
    loop.run_sync(lambda: update(config))
    print(config.renew_period)
    pc = PeriodicCallback(lambda: update(config), config.renew_period)
    pc.start()
