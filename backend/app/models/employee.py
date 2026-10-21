from datetime import date, datetime
from decimal import Decimal

from sqlalchemy import (
    CHAR,
    CheckConstraint,
    Date,
    DateTime,
    Identity,
    Numeric,
    String,
    func,
)
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base


class Employee(Base):
    __tablename__ = "employees"
    __table_args__ = (CheckConstraint("salary > 0", name="salary_positive"),)

    id: Mapped[int] = mapped_column(Identity(), primary_key=True)
    full_name: Mapped[str] = mapped_column(String(200))
    email: Mapped[str] = mapped_column(String(254), unique=True, index=True)
    job_title: Mapped[str] = mapped_column(String(100), index=True)
    department: Mapped[str] = mapped_column(String(100), index=True)
    country: Mapped[str] = mapped_column(CHAR(2), index=True)
    currency: Mapped[str] = mapped_column(CHAR(3))
    salary: Mapped[Decimal] = mapped_column(Numeric(12, 2))
    salary_usd: Mapped[Decimal] = mapped_column(Numeric(12, 2))
    hire_date: Mapped[date] = mapped_column(Date)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )
