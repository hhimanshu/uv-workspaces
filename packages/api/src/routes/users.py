from dto.user_dto import CreateUserRequest, UserResponse
from fastapi import APIRouter, Depends
from services.dependencies import get_user_service
from services.user_service import UserService
from src._lib.endpoints import ApiEndpoints
from src._lib.shared import ApiVersion, get_api_version


router = APIRouter(
    prefix=ApiEndpoints.API.USERS.path,
    tags=["users"],
    responses={404: {"description": "Not found"}},
)


@router.post("", response_model=UserResponse)
async def create_user(
    user_request: CreateUserRequest,
    user_service: UserService = Depends(get_user_service),
    api_version: ApiVersion = Depends(get_api_version),
):
    if api_version == ApiVersion.V2024_10_PREVIEW:
        return await user_service.create_user(user_request)
    return await user_service.create_user(user_request)
