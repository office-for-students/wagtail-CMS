#!/bin/bash
set -e

#Run Gunicorn
exec gunicorn CMS.wsgi:application \
  --name discover-uni-cms \
  --bind 0.0.0.0:80 \
  --workers 3 \
  --log-level=info \
  --log-file=- \
  --access-logfile=- \
  --error-logfile=- \
  --timeout 60


# EXECUTE DOCKER COMMAND NOW
exec "$@"
