from math import atan2, cos, radians, sin, sqrt

from sqlalchemy.orm import Session

from app.models.location import Location, LocationType, CoordinateSource
from app.utils.location_validation import validate_coordinates


def create_location(
    db: Session,
    name: str,
    address: str | None,
    latitude: float,
    longitude: float,
    location_type: LocationType | None = None,
    accuracy_meters: float | None = None,
    coordinate_source: CoordinateSource | None = None,
) -> Location:
    validate_coordinates(latitude, longitude)

    if accuracy_meters is not None and accuracy_meters < 0:
        raise ValueError("Accuracy must be greater than or equal to 0.")

    location = Location(
        name=name,
        address=address,
        location_type=location_type,
        latitude=latitude,
        longitude=longitude,
        accuracy_meters=accuracy_meters,
        coordinate_source=coordinate_source,
    )

    db.add(location)
    db.commit()
    db.refresh(location)

    return location


def get_location(
    db: Session,
    location_id: int,
) -> Location | None:
    return db.get(Location, location_id)


def update_location(
    db: Session,
    location_id: int,
    name: str,
    address: str | None,
    latitude: float,
    longitude: float,
) -> Location | None:
    location = db.get(Location, location_id)

    if location is None:
        return None

    validate_coordinates(latitude, longitude)

    location.name = name
    location.address = address
    location.latitude = latitude
    location.longitude = longitude

    db.commit()
    db.refresh(location)

    return location


def delete_location(
    db: Session,
    location_id: int,
) -> Location | None:
    location = db.get(Location, location_id)

    if location is None:
        return None

    db.delete(location)
    db.commit()

    return location


def calculate_distance(
    latitude1: float,
    longitude1: float,
    latitude2: float,
    longitude2: float,
) -> float:
    """
    Calculate the distance between two coordinates.

    Returns:
        Distance in kilometers.
    """

    earth_radius_km = 6371.0

    lat1 = radians(latitude1)
    lat2 = radians(latitude2)

    delta_lat = radians(latitude2 - latitude1)
    delta_lon = radians(longitude2 - longitude1)

    a = (
        sin(delta_lat / 2) ** 2
        + cos(lat1)
        * cos(lat2)
        * sin(delta_lon / 2) ** 2
    )

    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    return earth_radius_km * c


def find_nearby_locations(
    db: Session,
    latitude: float,
    longitude: float,
    radius_km: float,
) -> list[Location]:
    """
    Find locations within a given radius.

    Args:
        db: Database session.
        latitude: User's current latitude.
        longitude: User's current longitude.
        radius_km: Search radius in kilometers.

    Returns:
        A list of locations within the requested radius.
    """

    validate_coordinates(latitude, longitude)

    if radius_km <= 0:
        raise ValueError("Radius must be greater than 0.")

    locations = db.query(Location).all()

    nearby_locations = []

    for location in locations:
        distance = calculate_distance(
            latitude,
            longitude,
            location.latitude,
            location.longitude,
        )

        if distance <= radius_km:
            nearby_locations.append(location)

    return nearby_locations

