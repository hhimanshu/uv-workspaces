from fastapi import FastAPI, Request

from src._lib.custom_openapi import custom_openapi
from src._lib.endpoints import Endpoints
from src._lib.shared import ApiVersion, add_version_headers
from src.routes import hello, users


def create_app() -> FastAPI:
    app = FastAPI(
        title="Your API",
        description="API routes and mappings",
        root_path=Endpoints.API.path,
        docs_url=Endpoints.DOCS.path,
        openapi_url=Endpoints.OPENAPI.path,
    )

    @app.middleware("http")
    async def version_headers_middleware(request: Request, call_next):
        response = await call_next(request)
        api_version = getattr(request.state, "api_version", ApiVersion.LATEST)
        add_version_headers(response, api_version)
        return response

    app.include_router(hello.router)
    app.include_router(users.router)

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
