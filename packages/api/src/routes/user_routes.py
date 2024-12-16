from dto.user_dto import CreateUserRequest, UserResponse
from fastapi import APIRouter, Depends
from services.dependencies import get_user_service
from services.user_service import UserService

from src._lib.shared import ApiVersion, get_api_version


router = APIRouter(
    prefix="/users",
    tags=["users"],
    responses={404: {"description": "Not found"}},
)


""" @router.middleware("http")
async def version_headers_middleware(request: Request, call_next):
    response = await call_next(request)
    api_version = request.state.api_version
    add_version_headers(response, api_version)
    return response
 """


@router.post("/", response_model=UserResponse)
async def create_user(
    user_request: CreateUserRequest,
    user_service: UserService = Depends(get_user_service),
    api_version: ApiVersion = Depends(get_api_version),
):
    if api_version == ApiVersion.V2024_10_PREVIEW:
        return await user_service.create_user(user_request)
    return await user_service.create_user(user_request)
