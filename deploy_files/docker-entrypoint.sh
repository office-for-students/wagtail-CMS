#!/bin/bash
set -e

#until python3 manage.py makemigrations
#do
#  echo "Waiting for migrations to be created"
#  sleep 5
#done

until python3 manage.py migrate
do
  echo "Waiting for database to be migrated"
  sleep 5
done

#until python3 manage.py update_index
#do
#  echo "Waiting for search to be indexed"
#  sleep 5
#done

#Run Gunicorn
exec gunicorn CMS.wsgi:application \
    --name discover-uni-cms \
    --bind 0.0.0.0:80 \
    --worker-class gevent \
    --workers 8 \
    --worker-connections 300 \
    --timeout 120 \
    --graceful-timeout 30 \
    --max-requests 1000 \
    --max-requests-jitter 100 \
    --log-level warnning




# EXECUTE DOCKER COMMAND NOW
exec "$@"
