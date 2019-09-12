#!/bin/bash
set -e

until python3 manage.py migrate
do
  echo "Waiting for database to be migrated"
  sleep 5
done

#Run Gunicorn
exec gunicorn CMS.wsgi:application \
  --name discover-uni-cms \
  --bind 0.0.0.0:80 \
  --workers 10 \
  --log-level=info \
  --log-file=- \
  --access-logfile=- \
  --error-logfile=- \
  --timeout 60 \
  --max-requests 1000


# EXECUTE DOCKER COMMAND NOW
exec "$@"
