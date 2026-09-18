from pydantic import BaseModel, Field

from app.models.location import CoordinateSource, LocationType


class LocationCreate(BaseModel):
    name: str = Field(min_length=1, max_length=255)
    address: str | None = Field(default=None, max_length=500)
    latitude: float = Field(ge=-90, le=90)
    longitude: float = Field(ge=-180, le=180)
    location_type: LocationType | None = None
    accuracy_meters: float | None = Field(default=None, ge=0)
    coordinate_source: CoordinateSource | None = None


class LocationResponse(BaseModel):
    id: int
    name: str
    address: str | None
    latitude: float
    longitude: float
    location_type: LocationType | None
    accuracy_meters: float | None
    coordinate_source: CoordinateSource | None

    class Config:
        from_attributes = True