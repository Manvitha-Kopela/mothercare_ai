
from pydantic import BaseModel, Field


class MLPredictionRequest(BaseModel):
    age: float = Field(gt=0, le=100)
    systolic_bp: float = Field(gt=0, le=300)
    diastolic_bp: float = Field(gt=0, le=200)
    bs: float = Field(gt=0, le=50)
    body_temp: float = Field(gt=0, le=120)
    heart_rate: float = Field(gt=0, le=300)
