from typing import List

from fastapi import APIRouter, HTTPException
from starlette.responses import JSONResponse
from starlette.status import HTTP_204_NO_CONTENT, HTTP_503_SERVICE_UNAVAILABLE

from dtos.user_dto import UserDTO
from services.http_remote import get_users, get_user_by_id, create_user, update_user, delete_user

router = APIRouter(prefix="/user_operations", tags=["user_operations"])


@router.get("/user/{user_id}")
async def read_users(user_id: int) -> UserDTO:
    return await get_user_by_id(user_id)


@router.get("/users")
async def read_users() -> List[UserDTO]:
    return await get_users()


@router.post("/user")
async def create_users(user: UserDTO) -> JSONResponse:
    user_id = await create_user(user)
    return JSONResponse({"user_id": user_id})


@router.put("/user/{user_id}")
async def update_users(user: UserDTO) -> JSONResponse:
    await update_user(user)
    return JSONResponse({}, status_code=HTTP_204_NO_CONTENT)


@router.delete("/user/{user_id}")
async def delete_users(user_id: int) -> JSONResponse:
    await delete_user(user_id)
    return JSONResponse({}, status_code=HTTP_204_NO_CONTENT)


@router.get("/get_exception")
async def get_exception():
    raise HTTPException(status_code=HTTP_503_SERVICE_UNAVAILABLE)
