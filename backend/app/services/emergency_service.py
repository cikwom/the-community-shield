from math import radians, sin, cos, sqrt, atan2

from sqlalchemy.orm import Session

from app.models.emergency import EmergencyResource
from app.models.location import Location


def create_emergency_resource(
    db: Session,
    name: str,
    resource_type: str,
    location_id: int,
    organization_name: str | None = None,
) -> EmergencyResource:
    location = db.get(Location, location_id)

    if location is None:
        raise ValueError("Location not found")

    resource = EmergencyResource(
        name=name,
        resource_type=resource_type,
        location_id=location_id,
        organization_name=organization_name,
    )

    db.add(resource)
    db.commit()
    db.refresh(resource)

    return resource


def get_emergency_resource(
    db: Session,
    resource_id: int,
) -> EmergencyResource | None:
    return db.get(EmergencyResource, resource_id)


def get_emergency_resources(
    db: Session,
) -> list[EmergencyResource]:
    return db.query(EmergencyResource).all()


def get_emergency_resources_by_type(
    db: Session,
    resource_type: str,
) -> list[EmergencyResource]:
    return (
        db.query(EmergencyResource)
        .filter(EmergencyResource.resource_type == resource_type)
        .all()
    )


def find_nearby_emergency_resources(
    db: Session,
    latitude: float,
    longitude: float,
    radius_km: float,
) -> list[EmergencyResource]:
    locations = db.query(Location).all()

    nearby_location_ids = []

    earth_radius_km = 6371.0

    for location in locations:
        lat1 = radians(latitude)
        lon1 = radians(longitude)

        lat2 = radians(location.latitude)
        lon2 = radians(location.longitude)

        dlat = lat2 - lat1
        dlon = lon2 - lon1

        a = (
            sin(dlat / 2) ** 2
            + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
        )

        c = 2 * atan2(sqrt(a), sqrt(1 - a))

        distance_km = earth_radius_km * c

        if distance_km <= radius_km:
            nearby_location_ids.append(location.id)

    return (
        db.query(EmergencyResource)
        .filter(
            EmergencyResource.location_id.in_(nearby_location_ids)
        )
        .all()
    )