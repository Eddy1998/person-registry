from datetime import date

from sqlalchemy.orm import Session

from backend.models import PersonalData,  Residence


def get_personal_data_at(
    db: Session,
    person_id: int,
    reference_date: date,
) -> PersonalData | None:
    return (
        db.query(PersonalData)
        .filter(
            PersonalData.person_id == person_id,
            PersonalData.valid_from <= reference_date,
            PersonalData.valid_to >= reference_date,
        )
        .first()
    )

def get_residence_at(
    db: Session,
    person_id: int,
    reference_date: date,
) -> Residence | None:
    return (
        db.query(Residence)
        .filter(
            Residence.person_id == person_id,
            Residence.valid_from <= reference_date,
            Residence.valid_to >= reference_date,
        )
        .first()
    )