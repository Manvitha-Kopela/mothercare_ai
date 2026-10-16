
from fastapi import APIRouter, Depends, HTTPException

from app.rules_engine import assess, known_signs
from app.schemas.screening import ScreeningRequest
from app.services.auth_dependency import get_current_worker

router = APIRouter(
    prefix="/screening",
    tags=["Screening"],
)


@router.post("/assess")
def assess_screening(
    request: ScreeningRequest,
    current_worker=Depends(get_current_worker),
):
    allowed_signs = set(known_signs())
    unknown_signs = set(request.signs) - allowed_signs

    if unknown_signs:
        raise HTTPException(
            status_code=422,
            detail={
                "message": "Unknown danger-sign code(s)",
                "unknown_signs": sorted(unknown_signs),
            },
        )

    result = assess(request.signs)

    return {
        "tier": result.tier,
        "matched_rule_ids": result.matched_rule_ids,
        "matched_labels": result.matched_labels,
        "rules_reviewed": result.rules_reviewed,
        "rules_version": result.rules_version,
        "note": result.note,
        "disclaimer": (
            "Prototype decision support only. "
            "This result is not a diagnosis. "
            "Do not delay urgent clinical assessment or referral."
        ),
    }
