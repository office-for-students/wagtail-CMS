FROM python:3.6

ENV PYTHONUNBUFFERED 1
ENV DJANGO_ENV dev

WORKDIR /code
COPY ./requirements.txt /code/
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY . /code/

RUN useradd wagtail
RUN chown -R wagtail /code
USER wagtail
RUN chmod +x ./deploy_files/docker-entrypoint.sh

#RUN python manage.py compilescss
