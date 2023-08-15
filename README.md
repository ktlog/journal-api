# Journaling web application

[Inspiration](https://dayoneapp.com) - DayOne App, which I'm still using and happy about that.

I love to write thoughts in a notebook. This has many positive implications. 
But the most important thing is awareness, I live here and now, today will never happen again. 
This is important to remember.

---

The application is under development and now there is a minimal backend part.
The API documentaion is available [here](https://dayjournal.ru/docs).

### Stack:
- Fastapi
- Postgres + asyncpg (SQLAlchemy)
- React
- Typescript
- Docker, docker-compose

### Quickstart with Docker
1. Clone the repository:

```
git clone https://github.com/ktlog/journal-api.git
cd journal-api

```

2. Rename .env.dev to .env file  
in project root and set environment variables for application:

```
mv .env.dev .env
echo POSTGRES_PASSWORD=postgres >> .env
echo POSTGRES_USER=postgres >> .env
echo POSTGRES_DB=journaling >> .env
echo POSTGRES_HOST=db >> .env
echo POSTGRES_PORT=5432 >> .env

echo DATABASE_URL=postgresql+asyncpg://postgres:postgres@db:5432/journaling  >> .env

echo SERVER_HOST=127.0.0.1 >> .env
echo SERVER_PORT=8000 >> .env

echo JWT_SECRET=$(openssl rand -hex 16) >> .env
```

3. Finally, run:

```
docker compose up --build
```
