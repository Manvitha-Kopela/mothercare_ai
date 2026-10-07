from pydantic import BaseModel, Field


class HealthWorkerCreate(BaseModel):
    name: str = Field(min_length=2, max_length=100)
    mobile: str = Field(min_length=10, max_length=15)
    password: str = Field(min_length=6, max_length=128)
    role: str = Field(min_length=2, max_length=20)


class HealthWorkerResponse(BaseModel):
    id: int
    name: str
    mobile: str
    role: str
    is_active: bool

    class Config:
        from_attributes = True