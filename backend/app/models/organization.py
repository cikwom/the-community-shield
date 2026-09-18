from sqlalchemy import ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class Organization(Base):
    __tablename__ = "organizations"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        index=True
    )

    name: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )

    organization_type: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )

    description: Mapped[str | None] = mapped_column(
        Text,
        nullable=True
    )

    location_id: Mapped[int | None] = mapped_column(
        ForeignKey("locations.id"),
        nullable=True
    )

    location = relationship(
        "Location",
        back_populates="organizations"
    )

    emergency_resources = relationship(
        "Emergency",
        back_populates="organization"
    )
