# List Giftr

A web application for tracking gift ideas.

# Usage

There is a hosted version of the application available at https://listgiftr.com,
or the application may be self-hosted.

## Deployment

List Giftr is a Django application. You will need to be familiar with deploying
Django projects in order to run it.

### Environment Variables

The following environment variables are required in production:

**Name** | **Django Setting** | **Description**
---|---|---
`SECRET_KEY` | [`SECRET_KEY`][django-setting-secret-key] | Used for cryptographic signing operations such as encrypting session tokens
`ALLOWED_HOSTS` | [`ALLOWED_HOSTS`][django-setting-allowed-hosts] | Comma-separated list of hosts allowed to access the application
`CSRF_TRUSTED_ORIGINS` | [`CSRF_TRUSTED_ORIGINS`][django-setting-csrf-trusted-origins] | Comma-separated list of origins to accept unsafe operations (eg POST requests) from
`DB_NAME` | | Name of the database to connect to
`DB_USER` | | Username to connect to the database as
`DB_PASSWORD` | | Password for the database user
`DB_HOST` | | Hostname for the database
`DB_PORT` | | Port to connect to the database on

The following environment variables are optional in a production deployment:

**Name** | **Django Setting** | **Default** | **Description**
---|---|---|---
`DEFAULT_FROM_EMAIL` | [`DEFAULT_FROM_EMAIL`][django-setting-default-from-email] | `listgiftr@localhost` | Default email address to use as the "from" field in outgoing emails
`EMAIL_HOST` | [`EMAIL_HOST`][django-setting-email-host] | `None` | Host for sending SMTP emails. If not provided, emails are logged to `stdout`
`EMAIL_HOST_USER` | [`EMAIL_HOST_USER`][django-setting-email-host-user] | `None` | Username to authenticate SMTP emails
`EMAIL_HOST_PASSWORD` | [`EMAIL_HOST_PASSWORD`][django-setting-email-host-password] | `None` | Password to authenticate SMTP emails
`EMAIL_PORT` | [`EMAIL_PORT`][django-setting-email-port] | `587` | Port to send SMTP emails on
`EMAIL_USE_TLS` | [`EMAIL_USE_TLS`][django-setting-email-use-tls] | `True` | Whether to use TLS when talking to the SMTP server

The following environment variables can be used as flags to enable development
specific features. The following values (case insensitive) are accepted as
truthy: `t`, `true`, `y`, `yes`, `1`

**Name** | **Description**
---|---
`DEBUG` | Enables debug mode which provides stack traces in the browser when errors occur. This can expose sensitive information. This also provides a default value for `SECRET_KEY`.
`DEV_LIVE_RELOAD` | Enables live reloading of the browser when template changes are made.
`DEV_TOOLS` | Enables `django-debug-toolbar`
`DISABLE_PASSWORD_RESTRICTIONS` | Disables the requirement that passwords not be too common.

# Development

A devcontainer configuration is provided in the repository. The easiest way to
develop is to open it in VS Code.

The server can be run from the default launch configuration (<kbd>F5</kbd>).

Theming is handled by Tailwind, and needs a separate process to watch for
changes. First install the dependencies with:

```shell
./wishlists/manage.py tailwind install
```

Then run the watcher task to automatically rebuild the stylesheet based on the
classes referenced in the templates:

```shell
./wishlists/manage.py tailwind start
```


[django-setting-allowed-hosts]: https://docs.djangoproject.com/en/5.0/ref/settings/#allowed-hosts
[django-setting-csrf-trusted-origins]: https://docs.djangoproject.com/en/5.0/ref/settings/#csrf-trusted-origins
[django-setting-default-from-email]: https://docs.djangoproject.com/en/5.0/ref/settings/#default-from-email
[django-setting-email-host]: https://docs.djangoproject.com/en/5.0/ref/settings/#email-host
[django-setting-email-host-user]: https://docs.djangoproject.com/en/5.0/ref/settings/#email-host-user
[django-setting-email-host-password]: https://docs.djangoproject.com/en/5.0/ref/settings/#email-host-password
[django-setting-email-port]: https://docs.djangoproject.com/en/5.0/ref/settings/#email-port
[django-setting-email-use-tls]: https://docs.djangoproject.com/en/5.0/ref/settings/#email-use-tls
[django-setting-secret-key]: https://docs.djangoproject.com/en/5.0/ref/settings/#secret-key
