#!/bin/sh

set -euf

# Move into the application so Python imports resolve correctly
cd wishlists

# Execute system checks to ensure early exit if app is misconfigured
python manage.py check
# Run database migrations. This should be removed in favor of executing a
# separate migrations job if multiple app servers are deployed.
python manage.py migrate --no-input
# Collect static files to be served by proxy
python manage.py collectstatic --clear --no-input

exec gunicorn -b 0.0.0.0:8000 wishlists.wsgi
