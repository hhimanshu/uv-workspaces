from dto.user_dto import CreateUserRequest, UserResponse
from fastapi import APIRouter, Depends
from services.dependencies import get_user_service
from services.user_service import UserService


router = APIRouter(
    prefix="/users",
    tags=["users"],
    responses={404: {"description": "Not found"}},
)


@router.post("/", response_model=UserResponse)
async def create_user(
    user_request: CreateUserRequest,
    user_service: UserService = Depends(get_user_service),
):
    return await user_service.create_user(user_request)


# ...existing code for other user endpoints...
