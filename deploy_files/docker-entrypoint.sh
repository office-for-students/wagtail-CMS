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
#exec gunicorn CMS.wsgi:application \
#  --name discover-uni-cms \
#  --bind 0.0.0.0:80 \
#  --workers 4 \
#  --threads 2 \
#  --log-level=warning \
#  --log-file=- \
#  --access-logfile=- \
#  --error-logfile=- \
#  --timeout 60 \
#  --graceful-timeout 30 \
#  --max-requests 1000 \
#  --max-requests-jitter 50

exec gunicorn CMS.wsgi:application \
  --name discover-uni-cms \
  --bind 0.0.0.0:8000 \
  --worker-class gthread \
  --workers 4 \
  --threads 4 \
  --preload \
  --keep-alive 10 \
  --log-level=warning \
  --access-logfile=- \
  --error-logfile=- \
  --timeout 60 \
  --graceful-timeout 30 \
  --max-requests 5000 \
  --max-requests-jitter 200


# EXECUTE DOCKER COMMAND NOW
exec "$@"
