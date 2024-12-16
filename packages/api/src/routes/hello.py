from fastapi import APIRouter


router = APIRouter(
    prefix="/hello",
    tags=["hello"],
    responses={404: {"description": "Not found"}},
)


@router.get("/")
async def hello_world():
    """
    A simple hello world endpoint to verify the API is working.
    Returns:
        dict: A greeting message
    """
    return {"message": "Hello, World!"}


@router.get("/{name}")
async def hello_name(name: str):
    """
    Personalized greeting endpoint.
    Args:
        name (str): Name to greet
    Returns:
        dict: A personalized greeting message
    """

    return {"message": f"Hello, {name}!"}
