from app.services.location_service import (
    create_location,
    get_location,
    update_location,
    delete_location,
    find_nearby_locations,
)

router = APIRouter(
    prefix="/locations",
    tags=["Locations"],
)


@router.post("/", response_model=LocationResponse)
def create_new_location(
    location: LocationCreate,
    db: Session = Depends(get_db),
):
    return create_location(
        db=db,
        name=location.name,
        address=location.address,
        latitude=location.latitude,
        longitude=location.longitude,
        location_type=location.location_type,
        accuracy_meters=location.accuracy_meters,
        coordinate_source=location.coordinate_source,
    )


@router.get("/{location_id}", response_model=LocationResponse)
def read_location(
    location_id: int,
    db: Session = Depends(get_db),
):
    location = get_location(db, location_id)

    if location is None:
        raise HTTPException(
            status_code=404,
            detail="Location not found",
        )

    return location


@router.put("/{location_id}", response_model=LocationResponse)
def update_existing_location(
    location_id: int,
    location: LocationCreate,
    db: Session = Depends(get_db),
):
    updated_location = update_location(
        db=db,
        location_id=location_id,
        name=location.name,
        address=location.address,
        latitude=location.latitude,
        longitude=location.longitude,
    )

    if updated_location is None:
        raise HTTPException(
            status_code=404,
            detail="Location not found",
        )

    return updated_location


@router.delete("/{location_id}", response_model=LocationResponse)
def delete_existing_location(
    location_id: int,
    db: Session = Depends(get_db),
):
    deleted_location = delete_location(
        db=db,
        location_id=location_id,
    )

    if deleted_location is None:
        raise HTTPException(
            status_code=404,
            detail="Location not found",
        )

    return deleted_location
@router.get("/nearby", response_model=list[LocationResponse])
def nearby_locations(
    latitude: float,
    longitude: float,
    radius_km: float = 5,
    db: Session = Depends(get_db),
):
    return find_nearby_locations(
        db=db,
        latitude=latitude,
        longitude=longitude,
        radius_km=radius_km,
    )