from fastapi import Depends, FastAPI, HTTPException
from datetime import date
from sqlalchemy.orm import Session

from backend.database import get_db
from backend.models import Person, PersonalData, Residence
from backend.schemas import PersonCreate, PersonResponse, ResidenceCreate, ResidenceResponse
from backend.services import (
    get_personal_data_at,
    get_residence_at,
)


app = FastAPI(
    title="Person Registry API",
    version="1.0.0",
)


@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.post("/persons")
def create_person(
    data: PersonCreate, 
    db: Session = Depends(get_db)
):

    try:
        person = Person()

        db.add(person)
        db.flush()

        personal_data = PersonalData(
            person_id=person.id,
            first_name=data.first_name,
            last_name=data.last_name,
            tax_code=data.tax_code,
            valid_from=data.valid_from,
        )

        db.add(personal_data)
        db.commit()
        db.refresh(person)

        return {
            "id": person.id,
            "first_name": personal_data.first_name,
            "last_name": personal_data.last_name,
            "tax_code": personal_data.tax_code,
            "valid_from": personal_data.valid_from,
            "valid_to": personal_data.valid_to,
        }

    finally:
        db.close()

@app.get("/persons/{person_id}", response_model=PersonResponse)
def get_person(
    person_id: int,
    reference_date: date | None = None,
    db: Session = Depends(get_db),
):

    try:
        person = db.get(Person, person_id)

        if person is None:
            raise HTTPException(
                status_code=404,
                detail="Person not found",
            )
        
        target_date = reference_date or date.today()

        personal_data = get_personal_data_at(
            db,
            person.id,
            target_date,
        )

        if personal_data is None:
            raise HTTPException(
                status_code=404,
                detail="Personal data not found",
            )

        return PersonResponse(
            id=person.id,
            first_name=personal_data.first_name,
            last_name=personal_data.last_name,
            tax_code=personal_data.tax_code,
            valid_from=personal_data.valid_from,
            valid_to=personal_data.valid_to,
        )

    finally:
        db.close()

@app.post("/persons/{person_id}/residences")
def create_residence(
    person_id: int,
    data: ResidenceCreate,
    db: Session = Depends(get_db),
):

    try:
        person = db.get(Person, person_id)

        if person is None:
            raise HTTPException(
                status_code=404,
                detail="Person not found",
            )

        residence = Residence(
            person_id=person.id,
            street=data.street,
            city=data.city,
            postal_code=data.postal_code,
            valid_from=data.valid_from,
        )

        db.add(residence)
        db.commit()
        db.refresh(residence)

        return {
            "id": residence.id,
            "person_id": residence.person_id,
            "street": residence.street,
            "city": residence.city,
            "postal_code": residence.postal_code,
            "valid_from": residence.valid_from,
            "valid_to": residence.valid_to,
        }

    finally:
        db.close()

@app.get(
    "/persons/{person_id}/residence",
    response_model=ResidenceResponse,
)
def get_residence(
    person_id: int,
    reference_date: date | None = None,
    db: Session = Depends(get_db)
):

    try:
        person = db.get(Person, person_id)

        if person is None:
            raise HTTPException(
                status_code=404,
                detail="Person not found",
            )

        target_date = reference_date or date.today()

        residence = get_residence_at(
            db,
            person.id,
            target_date,
        )

        if residence is None:
            raise HTTPException(
                status_code=404,
                detail="No residence valid for the requested date",
            )

        return residence

    finally:
        db.close()