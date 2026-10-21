from decimal import ROUND_HALF_UP, Decimal

USD_PER_UNIT: dict[str, Decimal] = {
    "USD": Decimal("1"),
    "EUR": Decimal("1.08"),
    "GBP": Decimal("1.27"),
    "CAD": Decimal("0.73"),
    "AUD": Decimal("0.66"),
    "JPY": Decimal("0.0067"),
    "INR": Decimal("0.012"),
    "BRL": Decimal("0.18"),
}

CENT = Decimal("0.01")


class UnknownCurrencyError(ValueError):
    def __init__(self, currency: str) -> None:
        super().__init__(f"No exchange rate for currency {currency!r}")
        self.currency = currency


def to_usd(amount: Decimal, currency: str) -> Decimal:
    """Fixed demo rates, so insights and tests stay deterministic."""
    rate = USD_PER_UNIT.get(currency)
    if rate is None:
        raise UnknownCurrencyError(currency)
    return (amount * rate).quantize(CENT, rounding=ROUND_HALF_UP)
