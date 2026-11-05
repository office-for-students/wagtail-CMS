FROM python:3.14
ENV PYTHONUNBUFFERED 1
RUN mkdir /code
WORKDIR /code
COPY requirements.txt /code/
COPY requirements-deploy.txt /code/
RUN pip install -r requirements.txt  \
    && pip install -r requirements-deploy.txt
COPY . /code/


RUN cp /code/docker-compose.yml.example /code/docker-compose.yml
RUN python manage.py compilescss &&  \
    python manage.py collectstatic --noinput --ignore=*.scss

RUN chmod +x ./deploy_files/docker-entrypoint.sh
