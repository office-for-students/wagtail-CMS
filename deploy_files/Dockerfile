FROM python:3.13
ENV PYTHONUNBUFFERED 1
RUN mkdir /code
WORKDIR /code
COPY requirements.txt /code/
RUN pip install -r requirements.txt
COPY . /code/
RUN cp /code/docker-compose.yml.example /code/docker-compose.yml

RUN python manage.py compilescss
RUN python manage.py collectstatic --ignore=*.scss

RUN chmod +x ./deploy_files/docker-entrypoint.sh
