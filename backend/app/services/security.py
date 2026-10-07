from datetime import datetime, timedelta, timezone

from jose import jwt
from pwdlib import PasswordHash
from pydantic_settings import BaseSettings


class SecuritySettings(BaseSettings):
    jwt_secret_key: str

    class Config:
        env_file = ".env"
        extra = "ignore"


settings = SecuritySettings()


password_hash = PasswordHash.recommended()

SECRET_KEY = settings.jwt_secret_key
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60


def hash_password(password: str) -> str:
    return password_hash.hash(password)


def verify_password(password: str, hashed_password: str) -> bool:
    return password_hash.verify(password, hashed_password)


def create_access_token(data: dict) -> str:
    payload = data.copy()

    expire = datetime.now(timezone.utc) + timedelta(
        minutes=ACCESS_TOKEN_EXPIRE_MINUTES
    )

    payload.update({"exp": expire})

    return jwt.encode(
        payload,
        SECRET_KEY,
        algorithm=ALGORITHM,
    )