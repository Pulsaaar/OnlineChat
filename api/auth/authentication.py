from fastapi_users.authentication import BearerTransport, AuthenticationBackend, JWTStrategy
from fastapi_users import FastAPIUsers
from db.models import User
from .manager import get_user_manager
from config import AUTH_SECRET

SECRET = AUTH_SECRET


bearer_transport = BearerTransport(tokenUrl="auth/login")

def get_jwt_strategy() -> JWTStrategy:
    return JWTStrategy(secret=SECRET, lifetime_seconds=3600)

auth_backend = AuthenticationBackend(
    name="jwt",
    transport=bearer_transport,
    get_strategy=get_jwt_strategy,
)

fastapi_users = FastAPIUsers[User, int](
    get_user_manager,
    [auth_backend],
)

current_active_user = fastapi_users.current_user(active=True)
