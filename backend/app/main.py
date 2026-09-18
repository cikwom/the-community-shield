from fastapi import FastAPI

from app.database import Base, engine
from app.routers.location import router as location_router

from app.models import (
    Location,
    Organization,
    Emergency,
    LiveLocation,
)

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Community Shield API",
    description="Community safety and location API",
    version="1.0.0",
)

app.include_router(location_router)


@app.get("/")
def root():
    return {
        "message": "Community Shield API is running"
    }