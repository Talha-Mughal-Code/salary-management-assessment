from typing import Annotated, Literal

from pydantic import BaseModel, ConfigDict, Field, StringConstraints

from app.schemas.employee import CountryCode, EmployeeResponse

SortField = Literal[
    "full_name", "job_title", "department", "country", "salary_usd", "hire_date"
]
FilterText = Annotated[str, StringConstraints(strip_whitespace=True, max_length=200)]


class EmployeeListParams(BaseModel):
    page: int = Field(1, ge=1)
    page_size: int = Field(25, ge=1, le=100)
    q: FilterText | None = Field(None, description="Matches name or email.")
    country: CountryCode | None = None
    job_title: FilterText | None = None
    department: FilterText | None = None
    sort: SortField = "full_name"
    order: Literal["asc", "desc"] = "asc"


class EmployeePage(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    items: list[EmployeeResponse]
    total: int
    page: int
    page_size: int
