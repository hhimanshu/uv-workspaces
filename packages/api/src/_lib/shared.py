import logging
from datetime import datetime
from enum import Enum

from fastapi import FastAPI, Header, HTTPException
from fastapi.openapi.utils import get_openapi


logger = logging.getLogger(__name__)


class ApiVersion(str, Enum):
    # V2024_08_22 = "2024-08-22"
    V2024_10_PREVIEW = "2024-10-preview"
    LATEST = "latest"


VERSION_INFO = {
    # ApiVersion.V2023_05_01: {"deprecated": True, "sunset_date": "2024-05-01"},
    # ApiVersion.V2023_08_15: {"deprecated": True, "sunset_date": "2024-12-31"},
    # ApiVersion.V2024_01_01: {"deprecated": False, "sunset_date": None},
    # ApiVersion.V2024_08_22: {"deprecated": False, "sunset_date": None},
    ApiVersion.V2024_10_PREVIEW: {
        "deprecated": False,
        "sunset_date": None,
        "preview": True,
    },
}


def get_api_version(x_api_version: str | None = Header(None)) -> ApiVersion:
    if x_api_version is None or x_api_version == ApiVersion.LATEST:
        return ApiVersion.LATEST
    try:
        return ApiVersion(x_api_version)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid API version")


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
            for path in openapi_schema["paths"].values():
                for method in path.values():
                    method["parameters"] = [
                        {
                            "name": "X-API-VERSION",
                            "in": "header",
                            "required": False,
                            "schema": {
                                "type": "string",
                                "enum": [
                                    ApiVersion.V2024_10_PREVIEW,
                                    ApiVersion.LATEST,
                                ],
                            },
                        }
                    ] + (method.get("parameters", []))

            logger.debug("Setting OpenAPI schema")
            app.openapi_schema = openapi_schema

            # Modify the servers to include the /api prefix
            openapi_schema["servers"] = [{"url": "/api"}]
            app.openapi_schema = openapi_schema

            return app.openapi_schema
        except Exception as e:
            logger.error(f"Error generating OpenAPI schema: {str(e)}")
            raise

    return custom_openapi_func
