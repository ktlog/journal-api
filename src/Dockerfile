FROM python:3.11 as requirements-stage

WORKDIR /tmp

RUN pip install poetry

COPY pyproject.toml poetry.lock* /tmp/

RUN poetry export -f requirements.txt --output requirements.txt --without-hashes

FROM python:3.11

WORKDIR /journal_api

COPY --from=requirements-stage /tmp/requirements.txt requirements.txt

RUN pip install --no-cache-dir --upgrade -r requirements.txt

COPY . .

RUN chmod u+x docker/app.sh
