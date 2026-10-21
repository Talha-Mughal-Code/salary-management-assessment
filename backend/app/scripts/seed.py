import argparse
import random
import re
import sys
import unicodedata
from datetime import date, timedelta
from decimal import ROUND_HALF_UP, Decimal

from faker import Faker
from sqlalchemy import func, insert, select, text
from sqlalchemy.orm import Session

from app.core.database import get_engine
from app.core.fx import CENT, USD_PER_UNIT, to_usd
from app.models import Employee
from app.scripts.seed_data import (
    COUNTRIES,
    DEPARTMENT_WEIGHTS,
    US_BASE_SALARY_BY_TITLE,
    Country,
)

DEFAULT_COUNT = 10_000
DEFAULT_SEED = 42
CHUNK_SIZE = 1_000
EMAIL_DOMAIN = "acme.example"
HIRE_DATE_END = date(2026, 9, 30)
HIRE_WINDOW_DAYS = 12 * 365
SALARY_STEP = Decimal("100")


class ExistingEmployeesError(RuntimeError):
    def __init__(self, existing: int) -> None:
        super().__init__(
            f"The database already has {existing} employees. "
            "Run with --reset to replace them."
        )


def generate_employees(count: int, seed: int) -> list[dict]:
    rng = random.Random(seed)
    fake = Faker([country.locale for country in COUNTRIES])
    for offset, country in enumerate(COUNTRIES):
        fake.seed_locale(country.locale, seed + offset)
    country_weights = [country.weight for country in COUNTRIES]
    departments = list(DEPARTMENT_WEIGHTS)
    department_weights = list(DEPARTMENT_WEIGHTS.values())
    used_emails: set[str] = set()

    employees = []
    for _ in range(count):
        country = rng.choices(COUNTRIES, weights=country_weights)[0]
        department = rng.choices(departments, weights=department_weights)[0]
        job_title, us_base = rng.choice(
            list(US_BASE_SALARY_BY_TITLE[department].items())
        )
        first_name, last_name = _name(fake[country.locale], country.locale)
        salary = _local_salary(us_base, country, rng)
        hired_days_ago = rng.randint(0, HIRE_WINDOW_DAYS)
        employees.append(
            {
                "full_name": f"{first_name} {last_name}",
                "email": _unique_email(first_name, last_name, used_emails),
                "job_title": job_title,
                "department": department,
                "country": country.code,
                "currency": country.currency,
                "salary": salary,
                "salary_usd": to_usd(salary, country.currency),
                "hire_date": HIRE_DATE_END - timedelta(days=hired_days_ago),
            }
        )
    return employees


def seed_employees(session: Session, count: int, seed: int, reset: bool) -> int:
    existing = session.scalar(select(func.count()).select_from(Employee))
    if existing and not reset:
        raise ExistingEmployeesError(existing)
    if reset:
        session.execute(text(f"TRUNCATE {Employee.__tablename__} RESTART IDENTITY"))

    employees = generate_employees(count, seed)
    for start in range(0, len(employees), CHUNK_SIZE):
        session.execute(insert(Employee), employees[start : start + CHUNK_SIZE])
    return len(employees)


def _name(fake: Faker, locale: str) -> tuple[str, str]:
    """Japanese names are romanized so names and emails stay in Latin script."""
    if locale == "ja_JP":
        return fake.first_romanized_name(), fake.last_romanized_name()
    return fake.first_name(), fake.last_name()


def _local_salary(us_base: int, country: Country, rng: random.Random) -> Decimal:
    spread = Decimal(rng.randint(85, 120)) / 100
    local = Decimal(us_base) * country.pay_factor * spread
    local /= USD_PER_UNIT[country.currency]
    rounded = (local / SALARY_STEP).quantize(Decimal(1), rounding=ROUND_HALF_UP)
    return (rounded * SALARY_STEP).quantize(CENT)


def _unique_email(first_name: str, last_name: str, used: set[str]) -> str:
    local_part = f"{_slug(first_name)}.{_slug(last_name)}"
    email = f"{local_part}@{EMAIL_DOMAIN}"
    suffix = 2
    while email in used:
        email = f"{local_part}{suffix}@{EMAIL_DOMAIN}"
        suffix += 1
    used.add(email)
    return email


def _slug(value: str) -> str:
    ascii_value = unicodedata.normalize("NFKD", value).encode("ascii", "ignore")
    return re.sub(r"[^a-z]", "", ascii_value.decode().lower())


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Load demo employees.")
    parser.add_argument("--count", type=int, default=DEFAULT_COUNT)
    parser.add_argument("--seed", type=int, default=DEFAULT_SEED)
    parser.add_argument(
        "--reset", action="store_true", help="Delete all employees first."
    )
    args = parser.parse_args(argv)

    with Session(get_engine()) as session:
        try:
            inserted = seed_employees(session, args.count, args.seed, args.reset)
        except ExistingEmployeesError as error:
            print(error, file=sys.stderr)
            return 1
        session.commit()
    print(f"Inserted {inserted} employees.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
