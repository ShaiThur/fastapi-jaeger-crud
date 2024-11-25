from typing import List

from fastapi import HTTPException
from fastapi.routing import APIRouter
from starlette.responses import JSONResponse
from starlette.status import HTTP_204_NO_CONTENT, HTTP_400_BAD_REQUEST

from dtos.user_dto import UserDTO
from services import db
from configs.logging_config import logger

router = APIRouter(prefix="/db_user_operations", tags=["db_user_operations"])


@router.get("/user/{user_id}")
async def get_user(user_id: int) -> UserDTO:
    logger.info("get_user called")
    response = await db.get_user_async(user_id)
    if not response:
        raise HTTPException(status_code=HTTP_400_BAD_REQUEST)
    return response


@router.get("/users")
async def get_users() -> List[UserDTO]:
    logger.info("get_users called")
    return await db.get_all_user_async()


@router.post("/user")
async def create_user(user: UserDTO) -> JSONResponse:
    logger.info("create_user called")
    user_id = await db.create_user_async(user)
    return JSONResponse({"user_id": user_id})


@router.put("/user", status_code=HTTP_204_NO_CONTENT)
async def update_user(user_dto: UserDTO) -> None:
    logger.info("update_user called")
    await db.update_user_async(user_dto)


@router.delete("/user/{user_id}", status_code=HTTP_204_NO_CONTENT)
async def delete_user(user_id: int) -> None:
    logger.info("delete_user called")
    user = await db.get_user_async(user_id)
    if not user:
        raise HTTPException(status_code=HTTP_400_BAD_REQUEST)
    await db.delete_user_async(user_id)
