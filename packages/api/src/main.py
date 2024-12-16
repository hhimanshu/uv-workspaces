from fastapi import FastAPI
from src.routes import hello, user_routes


def create_app() -> FastAPI:
    app = FastAPI(
        title="Your API", description="API routes and mappings", version="0.1.0"
    )

    app.include_router(hello.router)
    app.include_router(user_routes.router)

    return app


app = create_app()
