from datetime import date, datetime

from sqlalchemy import Date, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.database.database import Base


class PregnantWoman(Base):
    __tablename__ = "pregnant_women"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        index=True,
    )

    name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    age: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    mobile: Mapped[str] = mapped_column(
        String(15),
        nullable=False,
    )

    address: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    lmp: Mapped[date | None] = mapped_column(
        Date,
        nullable=True,
    )

    edd: Mapped[date | None] = mapped_column(
        Date,
        nullable=True,
    )

    registered_by: Mapped[int] = mapped_column(
        ForeignKey("health_workers.id"),
        nullable=False,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
    )