from decimal import Decimal
from typing import NamedTuple


class Country(NamedTuple):
    code: str
    currency: str
    locale: str
    weight: int
    pay_factor: Decimal


COUNTRIES = [
    Country("US", "USD", "en_US", 30, Decimal("1.00")),
    Country("GB", "GBP", "en_GB", 12, Decimal("0.75")),
    Country("DE", "EUR", "de_DE", 12, Decimal("0.75")),
    Country("FR", "EUR", "fr_FR", 8, Decimal("0.65")),
    Country("ES", "EUR", "es_ES", 6, Decimal("0.55")),
    Country("CA", "CAD", "en_CA", 7, Decimal("0.80")),
    Country("AU", "AUD", "en_AU", 5, Decimal("0.80")),
    Country("JP", "JPY", "ja_JP", 6, Decimal("0.60")),
    Country("IN", "INR", "en_IN", 10, Decimal("0.25")),
    Country("BR", "BRL", "pt_BR", 4, Decimal("0.30")),
]

DEPARTMENT_WEIGHTS = {
    "Engineering": 30,
    "Sales": 18,
    "Customer Support": 15,
    "Marketing": 9,
    "Product": 8,
    "Finance": 7,
    "Operations": 7,
    "People": 6,
}

US_BASE_SALARY_BY_TITLE = {
    "Engineering": {
        "Software Engineer": 120_000,
        "Senior Software Engineer": 160_000,
        "Staff Engineer": 200_000,
        "Engineering Manager": 190_000,
        "QA Engineer": 95_000,
    },
    "Sales": {
        "Sales Development Representative": 60_000,
        "Account Executive": 90_000,
        "Sales Manager": 130_000,
    },
    "Customer Support": {
        "Support Specialist": 50_000,
        "Support Team Lead": 65_000,
    },
    "Marketing": {
        "Marketing Specialist": 70_000,
        "Content Strategist": 75_000,
        "Marketing Manager": 120_000,
    },
    "Product": {
        "Product Designer": 115_000,
        "Product Manager": 140_000,
        "Senior Product Manager": 170_000,
    },
    "Finance": {
        "Accountant": 70_000,
        "Financial Analyst": 85_000,
        "Finance Manager": 130_000,
    },
    "Operations": {
        "Operations Analyst": 75_000,
        "Operations Manager": 115_000,
    },
    "People": {
        "Recruiter": 70_000,
        "HR Generalist": 65_000,
        "HR Manager": 110_000,
    },
}
