from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.incident import (
    IncidentCreate,
    IncidentResponse,
)
from app.services.incident_service import (
    create_incident,
    get_incident,
    get_incidents,
    update_incident_status,
    find_nearby_resources_for_incident,
)


router = APIRouter(
    prefix="/incidents",
    tags=["Incidents"],
)


@router.post(
    "/",
    response_model=IncidentResponse,
)
def create_new_incident(
    incident: IncidentCreate,
    db: Session = Depends(get_db),
):
    return create_incident(db, incident)


@router.get(
    "/",
    response_model=list[IncidentResponse],
)
def get_all_incidents(
    db: Session = Depends(get_db),
):
    return get_incidents(db)


@router.get(
    "/{incident_id}",
    response_model=IncidentResponse,
)
def get_single_incident(
    incident_id: int,
    db: Session = Depends(get_db),
):
    incident = get_incident(db, incident_id)

    if incident is None:
        raise HTTPException(
            status_code=404,
            detail="Incident not found",
        )

    return incident


@router.put(
    "/{incident_id}/status",
    response_model=IncidentResponse,
)
def change_incident_status(
    incident_id: int,
    status: str,
    db: Session = Depends(get_db),
):
    incident = update_incident_status(
        db,
        incident_id,
        status,
    )

    if incident is None:
        raise HTTPException(
            status_code=404,
            detail="Incident not found",
        )

    return incident


@router.get(
    "/{incident_id}/nearby-resources",
)
def get_incident_nearby_resources(
    incident_id: int,
    radius_km: float = 5,
    db: Session = Depends(get_db),
):
    incident = get_incident(db, incident_id)

    if incident is None:
        raise HTTPException(
            status_code=404,
            detail="Incident not found",
        )

    return find_nearby_resources_for_incident(
        db=db,
        incident_id=incident_id,
        radius_km=radius_km,
    )