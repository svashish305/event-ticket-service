FROM python:3.10

WORKDIR /app

COPY ./alembic /app/alembic

COPY ./alembic.ini /app/alembic.ini

COPY ./requirements.txt /app/requirements.txt

RUN pip install --no-cache-dir -r /app/requirements.txt

COPY ./app /app/app