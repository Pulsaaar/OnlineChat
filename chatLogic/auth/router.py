from fastapi import APIRouter, Response, HTTPException
from fastapi import Depends
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordRequestForm
from .auth_back import auth_backend, fastapi_users
from models import User
from .schemas import UserCreate, UserRead

router = APIRouter(
    prefix="/auth",
    tags=["Auth"])


#Auth Router
router.include_router(
    fastapi_users.get_auth_router(auth_backend),
)

#Registration Router
router.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
)