from datetime import date

from sqlalchemy import Date, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.database import Base


class Person(Base):
    __tablename__ = "persons"

    id: Mapped[int] = mapped_column(primary_key=True)

    personal_data: Mapped[list["PersonalData"]] = relationship(
        back_populates="person",
        cascade="all, delete-orphan",
    )

    residences: Mapped[list["Residence"]] = relationship(
        back_populates="person",
        cascade="all, delete-orphan",
    )


    id: Mapped[int] = mapped_column(primary_key=True)

    person_id: Mapped[int] = mapped_column(
        ForeignKey("persons.id"),
        index=True,
    )

class PersonalData(Base):
    __tablename__ = "personal_data"

    id: Mapped[int] = mapped_column(primary_key=True)

    person_id: Mapped[int] = mapped_column(
        ForeignKey("persons.id"),
        index=True,
    )

    first_name: Mapped[str] = mapped_column(String(100))
    last_name: Mapped[str] = mapped_column(String(100))
    tax_code: Mapped[str] = mapped_column(
        String(16),
        index=True,
    )

    valid_from: Mapped[date] = mapped_column(Date)
    valid_to: Mapped[date] = mapped_column(Date)

    person: Mapped["Person"] = relationship(
        back_populates="personal_data",
    )


class Residence(Base):
    __tablename__ = "residences"

    id: Mapped[int] = mapped_column(primary_key=True)

    person_id: Mapped[int] = mapped_column(
        ForeignKey("persons.id"),
        index=True,
    )

    id: Mapped[int] = mapped_column(primary_key=True)

    person_id: Mapped[int] = mapped_column(
        ForeignKey("persons.id"),
        index=True,
    )

    street: Mapped[str] = mapped_column(String(200))
    city: Mapped[str] = mapped_column(String(100))
    postal_code: Mapped[str] = mapped_column(String(10))

    valid_from: Mapped[date] = mapped_column(Date)
    valid_to: Mapped[date] = mapped_column(Date)

    person: Mapped["Person"] = relationship(
        back_populates="residences",
    )