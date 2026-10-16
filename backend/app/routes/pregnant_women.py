from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.models.health_worker import HealthWorker
from app.models.pregnant_woman import PregnantWoman
from app.schemas.pregnant_woman import (
    PregnantWomanCreate,
    PregnantWomanResponse,
)
from app.services.auth_dependency import get_current_worker


router = APIRouter(
    prefix="/pregnant-women",
    tags=["Pregnant Women"],
)


@router.post(
    "/",
    response_model=PregnantWomanResponse,
)
def create_pregnant_woman(
    woman_data: PregnantWomanCreate,
    current_worker: HealthWorker = Depends(get_current_worker),
    db: Session = Depends(get_db),
):
    woman = PregnantWoman(
        name=woman_data.name,
        age=woman_data.age,
        mobile=woman_data.mobile,
        address=woman_data.address,
        lmp=woman_data.lmp,
        edd=woman_data.edd,
        registered_by=current_worker.id,
    )

    db.add(woman)
    db.commit()
    db.refresh(woman)

    return woman


@router.get(
    "/",
    response_model=list[PregnantWomanResponse],
)
def get_pregnant_women(
    current_worker: HealthWorker = Depends(get_current_worker),
    db: Session = Depends(get_db),
):
    woman = (
        db.query(PregnantWoman)
        .filter(PregnantWoman.registered_by == current_worker.id)
        .order_by(PregnantWoman.id.desc())
        .all()
    )

    return woman
