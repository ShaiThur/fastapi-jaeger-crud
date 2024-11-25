from pydantic import BaseModel


class UserDTO(BaseModel):
    user_id: int = 1
    name: str = "John"
    age: int = 0

