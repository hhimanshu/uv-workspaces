from fastapi import APIRouter, Depends

from src._lib.endpoints import ApiEndpoints
from src._lib.shared import ApiVersion, get_api_version


router = APIRouter(
    prefix=ApiEndpoints.HELLO.path,
    tags=["hello"],
    responses={404: {"description": "Not found"}},
)


@router.get(ApiEndpoints.HELLO.ROOT.path)
async def hello_world():
    """
    A simple hello world endpoint to verify the API is working.
    Returns:
        dict: A greeting message
    """
    return {"message": "Hello, World!"}


@router.get(ApiEndpoints.HELLO.NAME.path)
async def hello_name(
    name: str,
    api_version: ApiVersion = Depends(get_api_version),
):
    """
    Personalized greeting endpoint.
    Args:
        name (str): Name to greet
    Returns:
        dict: A personalized greeting message
    """

    if api_version == ApiVersion.V2024_10_PREVIEW:
        return {"message": f"Hello, {name}! (Preview)"}
    return {"message": f"Hello, {name}!"}
