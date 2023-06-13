FROM python:3.10

RUN apt update && apt upgrade -y

WORKDIR /app

COPY ./Pipfile /app/Pipfile
COPY ./Pipfile.lock /app/Pipfile.lock

RUN pip install pipenv
RUN --mount=type=ssh pipenv install --system --deploy

COPY . /app

EXPOSE 8000

RUN chmod +x scripts/start_api.sh
CMD scripts/start_api.sh
