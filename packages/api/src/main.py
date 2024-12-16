from fastapi import FastAPI

from src._lib.endpoints import Endpoints
from src._lib.shared import custom_openapi
from src.routes import hello, user_routes


def create_app() -> FastAPI:
    app = FastAPI(
        title="Your API",
        description="API routes and mappings",
        root_path=Endpoints.API.path,
        docs_url=Endpoints.DOCS.path,
        openapi_url=Endpoints.OPENAPI.path,
    )

    app.include_router(hello.router)
    app.include_router(user_routes.router)

    return app


app = create_app()
app.openapi = custom_openapi(app)


@app.get(Endpoints.ROOT.path)
async def root():
    return {"message": "Welcome to the API"}


@app.get(Endpoints.DEBUG.path)
async def debug_info():
    return {
        "openapi_url": app.openapi_url,
        "docs_url": app.docs_url,
        "routes": [{"path": route.path, "name": route.name} for route in app.routes],
    }
