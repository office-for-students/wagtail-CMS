FROM python:3.14

ENV PYTHONUNBUFFERED 1
ENV DJANGO_ENV dev
WORKDIR /code
COPY ./requirements.txt /code/
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY . /code/

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
