from datetime import date

from pydantic import BaseModel


class PersonCreate(BaseModel):
    first_name: str
    last_name: str
    tax_code: str
    valid_from: date


class PersonResponse(BaseModel):
    id: int
    first_name: str
    last_name: str
    tax_code: str
    valid_from: date
    valid_to: date

class ResidenceCreate(BaseModel):
    street: str
    city: str
    postal_code: str
    valid_from: date

class ResidenceResponse(BaseModel):
    id: int
    person_id: int
    street: str
    city: str
    postal_code: str
    valid_from: date
    valid_to: date