#!/bin/bash
echo "before alembic upgrade:" && alembic current
alembic upgrade head
exit_code=$?
if [ "${exit_code}" != "0" ]
then
    echo "Migration failed"
    exit $exit_code
fi
echo "after alembic upgrade:" && alembic current
uvicorn src.api.main:app --host 0.0.0.0 --port 8000
