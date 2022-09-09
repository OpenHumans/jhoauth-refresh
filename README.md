# JupyterHub OAuth2 Token Refresher

Jupyter notebook extension that periodically asks a [service](https://github.com/wildtreetech/ohjh/tree/master/images/refresher) for a token and
stores it in an environment variable.

## Install

Clone this repository and then:

```
pip install jhoauthrefresh
jupyter serverextension enable --py jhoauthrefresh
```

### Development install

```
pip install -e.
jupyter serverextension enable --py jhoauthrefresh
```

## Configuration

This extension is configured by customizing your jupyter_notebook_config.py file:

```
c.JHOauthRefreshConfig.jupyterhub_token_env_var = 'JUPYTERHUB_API_TOKEN'
c.JHOauthRefreshConfig.oauth_token_env_var = 'OAUTH_ACCESS_TOKEN'
c.JHOauthRefreshConfig.new_token_url = 'https://notebooks.openhumans.org/services/refresher/tokens'
c.JHOauthRefreshConfig.renew_period = 5000
```

Alternatively, parameters can be passed as command line arguments to Jupyter, as such:
```
jupyter lab --JHOauthRefreshConfig.oauth_token_env_var='JUPYTERHUB_API_TOKEN' --JHOauthRefreshConfig.renew_period=5000
```
