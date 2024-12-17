import logging
from datetime import datetime
from enum import Enum

from fastapi import FastAPI, Header, HTTPException, Request
from fastapi.openapi.utils import get_openapi


logger = logging.getLogger(__name__)


class ApiVersion(str, Enum):
    V2024_08_22 = "2024-08-22"
    V2024_10_PREVIEW = "2024-10-preview"
    LATEST = "latest"


VERSION_INFO = {
    # ApiVersion.V2023_05_01: {"deprecated": True, "sunset_date": "2024-05-01"},
    # ApiVersion.V2023_08_15: {"deprecated": True, "sunset_date": "2024-12-31"},
    # ApiVersion.V2024_01_01: {"deprecated": False, "sunset_date": None},
    ApiVersion.V2024_08_22: {"deprecated": False, "sunset_date": None},
    ApiVersion.V2024_10_PREVIEW: {
        "deprecated": False,
        "sunset_date": None,
        "preview": True,
    },
}


async def get_api_version(request: Request, x_api_version: str | None = Header(None)) -> ApiVersion:
    if x_api_version is None or x_api_version == ApiVersion.LATEST:
        api_version = ApiVersion.LATEST
    else:
        try:
            api_version = ApiVersion(x_api_version)
        except ValueError:
            raise HTTPException(status_code=400, detail="Invalid API version")

    request.state.api_version = api_version  # Store api_version in request.state
    return api_version


def add_version_headers(response, current_version: ApiVersion):
    version_info = VERSION_INFO.get(current_version, {})

    if version_info.get("deprecated"):
        response.headers["Deprecation"] = "true"
        response.headers["Link"] = (
            '<https://api.example.com/docs>; rel="deprecation"; type="text/html"'
        )
        response.headers["Warning"] = (
            f'299 - "This version is deprecated. Please upgrade to {ApiVersion.LATEST}"'
        )

    if version_info.get("sunset_date"):
        sunset_date = datetime.strptime(version_info["sunset_date"], "%Y-%m-%d")
        response.headers["Sunset"] = sunset_date.strftime("%a, %d %b %Y %H:%M:%S GMT")

    if version_info.get("preview"):
        response.headers["X-Version-Status"] = "Preview"


def custom_openapi(app: FastAPI):
    def custom_openapi_func():
        try:
            logger.debug("Generating custom OpenAPI schema")
            if app.openapi_schema:
                logger.debug("Returning cached OpenAPI schema")
                return app.openapi_schema

            openapi_schema = get_openapi(
                title="Your API",
                version="1.0.0",
                description="Your API description",
                routes=app.routes,
            )

            logger.debug("Adding version parameter to all endpoints")
            # Define the version parameter once at the components level
            openapi_schema["components"] = openapi_schema.get("components", {})
            openapi_schema["components"]["parameters"] = {
                "ApiVersionHeader": {
                    "name": "x-api-version",
                    "in": "header",
                    "required": False,
                    "schema": {
                        "type": "string",
                        "enum": [
                            ApiVersion.V2024_08_22,
                            ApiVersion.V2024_10_PREVIEW,
                            ApiVersion.LATEST,
                        ],
                        "default": ApiVersion.LATEST,
                    },
                    "description": "API Version to use",
                }
            }

            # Reference the parameter in all paths
            for path in openapi_schema["paths"].values():
                for method in path.values():
                    # Remove any existing x-api-version parameters
                    if "parameters" in method:
                        method["parameters"] = [
                            param
                            for param in method["parameters"]
                            if param.get("name", "").lower() != "x-api-version"
                        ]

                    # Add the reference to our component parameter
                    method["parameters"] = [
                        {"$ref": "#/components/parameters/ApiVersionHeader"}
                    ] + (method.get("parameters", []))

            # Modify the servers to include the /api prefix
            openapi_schema["servers"] = [{"url": "/api"}]
            app.openapi_schema = openapi_schema

            return app.openapi_schema
        except Exception as e:
            logger.error(f"Error generating OpenAPI schema: {str(e)}")
            raise

    return custom_openapi_func
