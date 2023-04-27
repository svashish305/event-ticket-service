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
```

## Run Instructions

```python
# run postgresql using docker compose
docker-compose up -d
# run server
uvicorn main:app --reload
```

## API Documentation

API documentation is available at http://localhost:8000/docs or http://localhost:8000/redoc