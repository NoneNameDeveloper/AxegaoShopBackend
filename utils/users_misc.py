from fastapi import HTTPException, Depends
from starlette.requests import Request

from database.models.token import Token
from database.models.user import User


async def get_current_user(request: Request) -> User | None:
    """получаем информацию о текущем пользователе по токену"""
    if not request.headers.get("Authorization"):
        return None

    token: str = request.headers.get("Authorization").split()[1]
    user: User = await (await Token.get(access_token=token)).get_user()

    if not user.is_active:
        raise HTTPException(status_code=404, detail="INACTIVE")
    return user


async def current_user_is_admin(user: User = Depends(get_current_user)):
    """проверка что это админ"""
    if not user:
        raise HTTPException(status_code=404, detail="UNAUTHORIZED")

    if not user.is_admin:
        raise HTTPException(status_code=403, detail="FORBIDDEN")

    return user
