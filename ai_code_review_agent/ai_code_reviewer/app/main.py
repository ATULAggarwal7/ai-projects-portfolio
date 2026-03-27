from fastapi import FastAPI
from app.api.routes import router

app = FastAPI(
    title="AI Code Review System",
    description="AI agent that reviews code according to company guidelines",
    version="1.0"
)

app.include_router(router)