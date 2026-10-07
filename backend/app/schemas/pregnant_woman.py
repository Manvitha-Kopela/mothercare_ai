from datetime import date

from pydantic import BaseModel, Field


class PregnantWomanCreate(BaseModel):
    name: str = Field(min_length=2, max_length=100)
    age: int = Field(ge=15, le=60)
    mobile: str = Field(min_length=10, max_length=15)
    address: str = Field(min_length=2, max_length=255)
    lmp: date | None = None
    edd: date | None = None


class PregnantWomanResponse(BaseModel):
    id: int
    name: str
    age: int
    mobile: str
    address: str
    lmp: date | None
    edd: date | None
    registered_by: int

    class Config:
        from_attributes = True