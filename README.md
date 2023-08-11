# Journaling web application

[Inspiration](https://dayoneapp.com) - DayOne App, which I'm still using and happy about that.

I love to write thoughts in a notebook. This has many positive implications. 
But the most important thing is awareness, I live here and now, today will never happen again. 
This is important to remember.
---
The application is under development and now there is a minimal backend part.
What the api looks like, you can see [here](http://www.sswaf.ru/docs).

### Stack:
- Fastapi
- Postgres (SQLAlchemy)
- React
- Typescript
- Docker, docker-compose

### Quickstart with Docker
1. Run the following commands to bootstrap your environment with poetry:
```
git clone https://github.com/ktlog/journal-api.git
cd journal-api
poetry install
poetry shell
```
2. Rename .env.dev to .env-prod file  
in project root and set environment variables for application:
```
mv .env.dev .env-prod
echo POSTGRES_PASSWORD=postgres >> .env-prod
echo POSTGRES_USER=postgres >> .env-prod
echo POSTGRES_DB=journaling >> .env-prod
echo POSTGRES_HOST=db >> .env-prod
echo POSTGRES_PORT=5432 >> .env-prod

echo DATABASE_URL=postgresql+asyncpg://postgres:postgres@db:5432/journaling  >> .env-prod

echo SERVER_HOST=127.0.0.1 >> .env-prod
echo SERVER_PORT=8000 >> .env-prod

echo JWT_SECRET=$(openssl rand -hex 16) >> .env-prod
```
3. Finally, run:
```
docker compose build
docker compose up
```
