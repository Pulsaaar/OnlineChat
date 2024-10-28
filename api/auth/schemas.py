from fastapi_users import schemas


class UserRead(schemas.BaseUser[int]):
    telegram_id: str

    class Config:
        from_attributes = True 

class UserCreate(schemas.BaseUserCreate):
    telegram_id: str
