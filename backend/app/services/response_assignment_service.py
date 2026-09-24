from sqlalchemy.orm import Session

from app.models.response_assignment import ResponseAssignment
from app.models.incident import Incident
from app.models.organization import Organization
from app.models.emergency import EmergencyResource
from app.models.live_location import LiveLocation


def create_response_assignment(
    db: Session,
    incident_id: int,
    organization_id: int,
    emergency_resource_id: int | None = None,
    responder_user_id: int | None = None,
):
    incident = db.get(Incident, incident_id)

    if not incident:
        raise ValueError("Incident not found")

    organization = db.get(Organization, organization_id)

    if not organization:
        raise ValueError("Organization not found")

    if emergency_resource_id is not None:
        emergency_resource = db.get(
            EmergencyResource,
            emergency_resource_id,
        )

        if not emergency_resource:
            raise ValueError("Emergency resource not found")

    assignment = ResponseAssignment(
        incident_id=incident_id,
        organization_id=organization_id,
        emergency_resource_id=emergency_resource_id,
        responder_user_id=responder_user_id,
        status="ASSIGNED",
    )

    db.add(assignment)
    db.commit()
    db.refresh(assignment)

    return assignment


def get_response_assignment(
    db: Session,
    assignment_id: int,
):
    return db.get(ResponseAssignment, assignment_id)


def get_response_assignments(
    db: Session,
):
    return (
        db.query(ResponseAssignment)
        .order_by(ResponseAssignment.assigned_at.desc())
        .all()
    )


def get_incident_response_assignments(
    db: Session,
    incident_id: int,
):
    return (
        db.query(ResponseAssignment)
        .filter(
            ResponseAssignment.incident_id == incident_id
        )
        .order_by(ResponseAssignment.assigned_at.desc())
        .all()
    )


def update_response_assignment_status(
    db: Session,
    assignment_id: int,
    status: str,
):
    assignment = db.get(
        ResponseAssignment,
        assignment_id,
    )

    if not assignment:
        return None

    assignment.status = status

    db.commit()
    db.refresh(assignment)

    return assignment


def delete_response_assignment(
    db: Session,
    assignment_id: int,
):
    assignment = db.get(
        ResponseAssignment,
        assignment_id,
    )

    if not assignment:
        return False

    db.delete(assignment)
    db.commit()

    return True


def get_responder_latest_live_location(
    db: Session,
    assignment_id: int,
):
    assignment = db.get(
        ResponseAssignment,
        assignment_id,
    )

    if not assignment:
        raise ValueError("Response assignment not found")

    if assignment.responder_user_id is None:
        return None

    return (
        db.query(LiveLocation)
        .filter(
            LiveLocation.user_id
            == assignment.responder_user_id
        )
        .order_by(
            LiveLocation.recorded_at.desc()
        )
        .first()
    )