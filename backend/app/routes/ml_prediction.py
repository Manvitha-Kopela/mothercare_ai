
from fastapi import APIRouter, Depends, HTTPException, status

from app.schemas.ml_prediction import MLPredictionRequest
from app.services.auth_dependency import get_current_worker
from app.services.ml_prediction import predict_risk

router = APIRouter(
    prefix="/ml",
    tags=["Experimental ML Prediction"],
)


@router.post("/predict")
def predict_maternal_risk(
    request: MLPredictionRequest,
    current_worker=Depends(get_current_worker),
):
    try:
        result = predict_risk(
            age=request.age,
            systolic_bp=request.systolic_bp,
            diastolic_bp=request.diastolic_bp,
            bs=request.bs,
            body_temp=request.body_temp,
            heart_rate=request.heart_rate,
        )
        return result

    except FileNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Experimental prediction model is not available.",
        )
