# Event Ticket Service

A project to demonstrate event ticketing system built using FastApi and PostgreSQL. It uses SQLAlchemy as ORM layer and alembic for running database migrations. Deployed locally using docker.

## Run Instructions

```python
# build docker image of fastapi and postgresql using docker compose
docker compose up --build
# if you face port already in use or permission denied, since docker also uses port 5432, stop local postgresql and run below command
sudo systemctl stop postgresql
# run both app and db in detached mode
sudo docker compose up -d
# check logs
sudo docker compose logs
```

## (Optional) Local Setup Instructions

```python
python3 -m venv .venv
source .venv/bin/activate
# install all dependencies
pip install -r requirements.txt
# (optional) set initial migration to create tables (first time only)
alembic init alembic
# this below command is to be executed after running database in docker container and before running server
# (follow run instructions on how to start postgresql database using docker) runs all database migrations 
# specified in versions folder which is auto generated by alembic and 
# edited later to perform upgrade() and downgrade(), this is to create tables and seed db with initial data 
alembic upgrade head
# (optional) in case of updating dependencies, after updates, run below command to update requirements.txt
pip freeze > requirements.txt
# (optional) after any model schema change, run below command with proper message to create another migration
alembic revision -m "custom message for next migration attempt"
alembic upgrade head
# (optional) run server locally
uvicorn app.main:app --reload
```

## API Documentation

API documentation is available at [OpenAPI](http://localhost:8000/docs) or [Redoc](http://localhost:8000/redoc)
Use this to refer to API endpoints and their request/response formats, to test them using OpenAPI UI or Postman or any other API Client tool.
