from traitlets import Unicode, Integer
from traitlets.config import Configurable


class JHOauthRefreshConfig(Configurable):
    """
    A Configurable that declares the configuration options
    for the jhoauthrefresh.
    """

    jupyterhub_token_env_var = Unicode(
        "JUPYTERHUB_API_TOKEN",
        config=True,
        help="Name of the environment variable storing JuyterHub API token.",
    )
    oauth_token_env_var = Unicode(
        "OAUTH_ACCESS_TOKEN",
        config=True,
        help="Name of the environment variable storing refreshing OAuth token.",
    )
    new_token_url = Unicode(
        "https://notebooks.openhumans.org/services/refresher/tokens",
        config=True,
        help="URL of the JupyterHub service providing refreshed token.",
    )
    # renew_period sets the period properly based on expiry time of the token
    # the period has to be specified in milliseconds
    # for example, for tokens that expire after ten hours, you can set
    # the variable to 1e3 * 60 * 60 * 8.5 (8.5 hours)
    renew_period = Integer(
        default_value=3600000,
        config=True,
        help="Time between token refreshes in milliseconds.",
    )
    extension_endpoint = Unicode(
        "oauth-token",
        config=True,
        help="Jupyter Server extension endpoint.",
    )
