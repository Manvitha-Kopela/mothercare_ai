from pydantic import BaseModel, Field


class LoginRequest(BaseModel):
    mobile: str = Field(min_length=10, max_length=15)
    password: str = Field(min_length=6, max_length=128)


class LoginResponse(BaseModel):
    access_token: str
    token_type: str
    health_worker_id: int
    name: str
    role: str