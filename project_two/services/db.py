from typing import List

from automapper import mapper
from opentelemetry.instrumentation.sqlalchemy import SQLAlchemyInstrumentor
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from dtos.user_dto import UserDTO
from models.user_model import UserModel
from configs.logging_config import logger

# TODO: не забыть вынести все подобные строки в .env
engine = create_async_engine("postgresql+asyncpg://postgres:artur123@host.docker.internal:5433/aiplatform")
# engine = create_async_engine("postgresql+asyncpg://postgres:artur123@localhost:5432/aiplatform")
SQLAlchemyInstrumentor().instrument(engine=engine.sync_engine)


def get_session():
    session_local = async_sessionmaker(bind=engine, expire_on_commit=False)
    return session_local()


async def get_user_async(user_id: int) -> UserDTO:
    conn = get_session()
    async with conn as session:
        async with session as sess:
            user = await sess.execute(select(UserModel).where(UserModel.id == user_id))
            user = user.scalars().first()
            if user:
                user_dto = mapper.to(UserDTO).map(user, fields_mapping={"user_id": user.id})
                logger.info(f"get user {user_dto} from db")
                return user_dto
            # TODO: добавить нормальный exception handler и не возвращать null
            logger.error(f"get user None from db")
            return None


async def get_all_user_async() -> List[UserDTO]:
    conn = get_session()
    async with conn as session:
        async with session as sess:
            users = await sess.execute(select(UserModel))
            users = users.scalars().all()
            dtos = []
            for user in users:
                dtos.append(mapper.to(UserDTO).map(user, fields_mapping={"user_id": user.id}))
            logger.info(f"get all users {dtos}")
            return dtos


async def create_user_async(user_dto: UserDTO) -> int:
    conn = get_session()
    async with conn as session:
        async with session as sess:
            user = mapper.to(UserModel).map(user_dto)
            sess.add(user)
            await sess.commit()
            await sess.refresh(user)
            logger.info(f"create user {user.id}")
            return user.id


async def update_user_async(user_dto: UserDTO) -> None:
    conn = get_session()
    async with conn as session:
        async with session as sess:
            await sess.execute(
                update(UserModel)
                .where(UserModel.id == user_dto.user_id)
                .values(name=user_dto.name, age=user_dto.age)
            )
            logger.info(f"update user {user_dto.user_id}")
            await sess.commit()


async def delete_user_async(user_id: int) -> None:
    conn = get_session()
    async with conn as session:
        async with session as sess:
            user = await sess.execute(select(UserModel).where(UserModel.id == user_id))
            await sess.delete(user.scalars().one_or_none())
            logger.info(f"delete user {user_id}")
            await sess.commit()
