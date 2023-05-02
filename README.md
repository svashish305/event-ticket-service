# Event Ticket Service

A project to demonstrate event ticketing system built using FastApi and PostgreSQL.

## Setup Instructions

```python
python3 -m venv .venv
source .venv/bin/activate
# first time, install fastapi and uvicorn if not already installed
pip install fastapi
pip install "uvicorn[standard]"
# second time onwards, install all dependencies
pip install -r requirements.txt
# in case of updating dependencies, after updates, run below command to update requirements.txt
pip freeze > requirements.txt
# rub db migrate/seed db
alembic revision --autogenerate -m "initial migration"
alembic revision -m "custom message for next migration attempt"
alembic upgrade head
```

## Run Instructions

```python
# run postgresql using docker compose
docker compose up -d
# if you face port already in use or permission denied, since docker also uses port 5432, stop docker and run below command
sudo systemctl stop postgresql
sudo docker compose up -d
# run server in separate terminal tab
source .venv/bin/activate
uvicorn app.main:app --reload
```

## API Documentation

API documentation is available at http://localhost:8000/docs or http://localhost:8000/redoc