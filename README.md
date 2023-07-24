# Large Language Model Chat Hub
LLMChatHub is an open-source project that serves as a centralized hub for 
deploying and managing multiple chatbots powered by Large Language Models (LLMs). 
It provides a flexible and efficient way to store and access different 
chatbot instances through a PostgreSQL database and offers a REST API 
for seamless interactions using FastAPI.

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

## Run Generation locally

### Using Service
Run the service and send requests to it.
<TODO: More on this>

### Using CLI
edit examples at the end of the file `src.services.chatbot` and then run:
```
pipenv run python3 -m src.services.chatbot
```

_Note: make sure `.env` file created as mentioned in the section above. 
And set the value of `OPENAI_API_KEY` in `.env` file._