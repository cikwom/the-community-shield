from math import asin, cos, radians, sin, sqrt

from sqlalchemy.orm import Session

from app.models.emergency import EmergencyResource
from app.models.incident import Incident
from app.schemas.incident import IncidentCreate


def create_incident(
    db: Session,
    incident_data: IncidentCreate,
) -> Incident:
    incident = Incident(
        title=incident_data.title,
        description=incident_data.description,
        incident_type=incident_data.incident_type,
        severity=incident_data.severity,
        status=incident_data.status,
        location_id=incident_data.location_id,
        reporter_id=incident_data.reporter_id,
        reported_at=incident_data.reported_at,
    )

    db.add(incident)
    db.commit()
    db.refresh(incident)

    return incident


def get_incident(
    db: Session,
    incident_id: int,
) -> Incident | None:
    return db.get(Incident, incident_id)


def get_incidents(
    db: Session,
) -> list[Incident]:
    return db.query(Incident).all()


def update_incident_status(
    db: Session,
    incident_id: int,
    status: str,
) -> Incident | None:
    incident = db.get(Incident, incident_id)

    if incident is None:
        return None

    incident.status = status

    db.commit()
    db.refresh(incident)

    return incident


def find_nearby_resources_for_incident(
    db: Session,
    incident_id: int,
    radius_km: float,
) -> list[EmergencyResource]:
    incident = db.get(Incident, incident_id)

    if incident is None:
        return []

    location = incident.location

    if location is None:
        return []

    resources = db.query(EmergencyResource).all()

    nearby_resources = []

    earth_radius_km = 6371.0

    for resource in resources:
        resource_location = resource.location

        if resource_location is None:
            continue

        lat1 = radians(location.latitude)
        lat2 = radians(resource_location.latitude)

        delta_lat = radians(
            resource_location.latitude - location.latitude
        )

        delta_lon = radians(
            resource_location.longitude - location.longitude
        )

        a = (
            sin(delta_lat / 2) ** 2
            + cos(lat1)
            * cos(lat2)
            * sin(delta_lon / 2) ** 2
        )

        distance = (
            2
            * earth_radius_km
            * asin(sqrt(a))
        )

        if distance <= radius_km:
            nearby_resources.append(resource)

    return nearby_resources