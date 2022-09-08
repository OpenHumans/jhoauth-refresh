# JupyterHub OAuth2 Token Refresher

Jupyter notebook extension that periodically asks a service for a token and
stores it in an environment variable.

## Install

Clone this repository and then:

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
c.JHOauthRefreshConfig.renew_period = 1
```
