#!/bin/bash
set -e

#until python3 manage.py migrate
#do
#  echo "Waiting for database to be migrated"
#  sleep 5
#done

#until python3 manage.py update_index
#do
#  echo "Waiting for search to be indexed"
#  sleep 5
#done

#Run Gunicorn
exec gunicorn CMS.wsgi:application \
  --bind 0.0.0.0:80 \
  --workers 8 \
  --threads 1 \
  --timeout 120


# EXECUTE DOCKER COMMAND NOW
exec "$@"
