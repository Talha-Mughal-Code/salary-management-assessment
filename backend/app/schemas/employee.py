from datetime import date, datetime
from decimal import Decimal
from typing import Annotated

from pydantic import (
    AfterValidator,
    BaseModel,
    ConfigDict,
    Field,
    StringConstraints,
    field_validator,
)

from app.core.fx import USD_PER_UNIT


def _supported_currency(code: str) -> str:
    if code not in USD_PER_UNIT:
        raise ValueError(f"must be one of {', '.join(USD_PER_UNIT)}")
    return code


FullName = Annotated[
    str, StringConstraints(strip_whitespace=True, min_length=1, max_length=200)
]
Label = Annotated[
    str, StringConstraints(strip_whitespace=True, min_length=1, max_length=100)
]
Email = Annotated[
    str,
    StringConstraints(
        strip_whitespace=True, max_length=254, pattern=r"^[^@\s]+@[^@\s]+\.[^@\s]+$"
    ),
]
CountryCode = Annotated[
    str,
    StringConstraints(strip_whitespace=True, to_upper=True, pattern=r"^[A-Za-z]{2}$"),
]
CurrencyCode = Annotated[
    str,
    StringConstraints(strip_whitespace=True, to_upper=True),
    AfterValidator(_supported_currency),
]
Salary = Annotated[Decimal, Field(gt=0, max_digits=12, decimal_places=2)]


class EmployeeCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    full_name: FullName
    email: Email
    job_title: Label
    department: Label
    country: CountryCode
    currency: CurrencyCode
    salary: Salary
    hire_date: date


class EmployeeUpdate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    full_name: FullName | None = None
    email: Email | None = None
    job_title: Label | None = None
    department: Label | None = None
    country: CountryCode | None = None
    currency: CurrencyCode | None = None
    salary: Salary | None = None
    hire_date: date | None = None

    @field_validator("*", mode="before")
    @classmethod
    def reject_null(cls, value: object) -> object:
        """Fields may be left out, but every column is required, so null is not."""
        if value is None:
            raise ValueError("may be omitted but not null")
        return value


class EmployeeResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    full_name: str
    email: str
    job_title: str
    department: str
    country: str
    currency: str
    salary: Decimal
    salary_usd: Decimal
    hire_date: date
    created_at: datetime
    updated_at: datetime
