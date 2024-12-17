import logging
from datetime import datetime
from enum import Enum

from fastapi import Header, HTTPException, Request


logger = logging.getLogger(__name__)


class ApiVersion(str, Enum):
    V2024_08_22 = ("2024-08-22", False, None, False)
    V2024_10_PREVIEW = ("2024-10-preview", False, None, True)
    LATEST = ("latest", False, None, False)

    def __new__(cls, value, deprecated, sunset_date, preview):
        obj = str.__new__(cls, value)
        obj._value_ = value
        obj.deprecated = deprecated
        obj.sunset_date = sunset_date
        obj.preview = preview
        return obj


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
    if current_version.deprecated:
        response.headers["Deprecation"] = "true"
        response.headers["Link"] = (
            '<https://api.example.com/docs>; rel="deprecation"; type="text/html"'
        )
        response.headers["Warning"] = (
            f'299 - "This version is deprecated. Please upgrade to {ApiVersion.LATEST.value}"'
        )

    if current_version.sunset_date:
        sunset_date = datetime.strptime(current_version.sunset_date, "%Y-%m-%d")
        response.headers["Sunset"] = sunset_date.strftime("%a, %d %b %Y %H:%M:%S GMT")

    if current_version.preview:
        response.headers["X-Version-Status"] = "Preview"
