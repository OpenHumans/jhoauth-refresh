import os
import json
import urllib

from tornado import web
from tornado.ioloop import IOLoop
from tornado.ioloop import PeriodicCallback
from tornado.httpclient import AsyncHTTPClient, HTTPRequest

from notebook.utils import url_path_join
from notebook.base.handlers import IPythonHandler


class TokenHandler(IPythonHandler):
    @web.authenticated
    async def get(self):
        self.write(os.getenv('OH_ACCESS_TOKEN'))


def setup_handlers(web_app):
    web_app.add_handlers('.*', [
        (url_path_join(web_app.settings['base_url'], 'oh-token'), TokenHandler)
        ])


async def fetch_new_token(token_url, client_id, client_secret, refresh_token):
    params = {"grant_type": "refresh_token",
              "client_id": client_id,
              "client_secret": client_secret,
              "refresh_token": refresh_token,
              }
    body = urllib.parse.urlencode(params)
    req = HTTPRequest(token_url, 'POST', body=body)

    client = AsyncHTTPClient()
    resp = await client.fetch(req)

    resp_json = json.loads(resp.body.decode('utf8', 'replace'))
    return resp_json


async def update():
    tokens = await fetch_new_token(os.getenv('OH_OAUTH2_TOKEN_URL'),
                                   os.getenv('OH_CLIENT_ID'),
                                   os.getenv('OH_CLIENT_SECRET'),
                                   os.getenv('OH_REFRESH_TOKEN'),)
    os.environ['OH_ACCESS_TOKEN'] = tokens['access_token']
    os.environ['OH_REFRESH_TOKEN'] = tokens['refresh_token']


def _jupyter_server_extension_paths():
    return [{
        'module': 'jhoauthrefresh',
        }]


def load_jupyter_server_extension(nbapp):
    """
    Called when the extension is loaded.
    """
    setup_handlers(nbapp.web_app)

    # update once at teh start to handle the case where the server is
    # being started so long after the login that the token itself has
    # expired so we need to refresh it straight away
    loop = IOLoop.current()
    loop.run_sync(update)
    # XXX set the period properly based on expiry time of the token
    # the period has to be specified in milliseconds
    # OpenHumans tokens expire after ten hours, we renew every 8.5h
    pc = PeriodicCallback(update, 1e3 * 60 * 60 * 8.5)
    pc.start()
