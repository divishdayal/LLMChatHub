# llm_magic

## Setting up environment for Local Development
Pipenv environment is used to install dependencies and run this repo.

1. Install packages:
```
pipenv install --dev
```

2. Setup Postgres DB:
```
docker-compose up -d pg
pipenv run alembic upgrade head
```
3. Setup application settings. Create `.env` file to customize settings. `env.SAMPLE` is provided with default values, 
which can be copied to `.env` to begin with. 
4. Run the service:
```
pipenv run uvicorn src.api.main:app --reload --host 0.0.0.0 --port 8000
```
