from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.models.health_worker import HealthWorker
from app.schemas.auth import LoginRequest, LoginResponse
from app.services.security import (
    create_access_token,
    verify_password,
)


router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)


@router.post(
    "/login",
    response_model=LoginResponse,
)
def login(
    login_data: LoginRequest,
    db: Session = Depends(get_db),
):
    worker = (
        db.query(HealthWorker)
        .filter(HealthWorker.mobile == login_data.mobile)
        .first()
    )

    if not worker:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid mobile number or password.",
        )

    if not worker.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="This health worker account is inactive.",
        )

    if not verify_password(
        login_data.password,
        worker.password_hash,
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid mobile number or password.",
        )

    access_token = create_access_token(
        {
            "sub": str(worker.id),
            "role": worker.role,
        }
    )

    return LoginResponse(
        access_token=access_token,
        token_type="bearer",
        health_worker_id=worker.id,
        name=worker.name,
        role=worker.role,
    )