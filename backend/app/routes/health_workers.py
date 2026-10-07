from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.models.health_worker import HealthWorker
from app.schemas.health_worker import (
    HealthWorkerCreate,
    HealthWorkerResponse,
)
from app.services.security import hash_password


router = APIRouter(
    prefix="/health-workers",
    tags=["Health Workers"],
)


@router.post(
    "/register",
    response_model=HealthWorkerResponse,
)
def register_health_worker(
    worker_data: HealthWorkerCreate,
    db: Session = Depends(get_db),
):
    existing_worker = (
        db.query(HealthWorker)
        .filter(HealthWorker.mobile == worker_data.mobile)
        .first()
    )

    if existing_worker:
        raise HTTPException(
            status_code=400,
            detail="A health worker with this mobile number already exists.",
        )

    worker = HealthWorker(
        name=worker_data.name,
        mobile=worker_data.mobile,
        password_hash=hash_password(worker_data.password),
        role=worker_data.role,
    )

    db.add(worker)
    db.commit()
    db.refresh(worker)

    return worker