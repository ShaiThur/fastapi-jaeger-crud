from typing import List

import httpx
from automapper import mapper

from dtos.user_dto import UserDTO
from configs.logging_config import logger


async def get_user_by_id(user_id: int) -> UserDTO:
    async with httpx.AsyncClient() as client:
        res = await client.get(f"http://host.docker.internal:8001/db_user_operations/user/{user_id}")
        user = mapper.to(UserDTO).map(res.json())
        logger.info(f"user {user}")
        return user


async def get_users() -> List[UserDTO]:
    async with httpx.AsyncClient() as client:
        users_list = []
        res = await client.get("http://host.docker.internal:8001/db_user_operations/users")

        for user in res.json():
            users_list.append(mapper.to(UserDTO).map(user))

        return users_list


async def create_user(user: UserDTO) -> int:
    async with httpx.AsyncClient() as client:
        res = await client.post(
            "http://host.docker.internal:8001/db_user_operations/user",
            json=user.model_dump_json()
        )
        user_id = res.json()
        logger.info(f"user_id after create: {user_id}")
        return user_id


async def update_user(user: UserDTO) -> int:
    async with httpx.AsyncClient() as client:
        res = await client.put(
        "http://host.docker.internal:8001/db_user_operations/user",
            json=user.model_dump_json()
        )
        user_id = res.json().get("user_id", 0)
        logger.info(f"user_id after update: {user_id}")
        return user_id


async def delete_user(user_id):
    async with httpx.AsyncClient() as client:
        await client.delete(f"http://host.docker.internal:8001/db_user_operations/user/{user_id}")
        logger.info(f"deleted user {user_id}")
