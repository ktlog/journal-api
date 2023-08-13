from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api import router


app = FastAPI(
    title='Journaling API',
    version='1.0',
    description='API for journaling life events',
    docs_url='/docs',
    redoc_url='/redoc',
)

origins = [
    'http://localhost:3000',
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS", "DELETE", "PATCH", "PUT"],
    allow_headers=["Content-Type", "Set-Cookie", "Access-Control-Allow-Headers", "Access-Control-Allow-Origin",
                   "Authorization"],
)


@app.get("/", include_in_schema=False)
async def root():
    return {"message": "The API documentation is available at /docs"}


app.include_router(router)
