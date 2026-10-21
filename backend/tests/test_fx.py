from decimal import Decimal

import pytest

from app.core.fx import UnknownCurrencyError, to_usd


def test_usd_is_unchanged():
    assert to_usd(Decimal("85000.00"), "USD") == Decimal("85000.00")


def test_converts_at_the_fixed_rate():
    assert to_usd(Decimal("60000.00"), "EUR") == Decimal("64800.00")


def test_low_value_currency_converts_to_cents():
    assert to_usd(Decimal("10000"), "JPY") == Decimal("67.00")


def test_half_cent_rounds_up():
    assert to_usd(Decimal("1000.25"), "AUD") == Decimal("660.17")


def test_result_has_two_decimal_places():
    assert to_usd(Decimal("1234.56"), "INR").as_tuple().exponent == -2


def test_unknown_currency_raises():
    with pytest.raises(UnknownCurrencyError) as error:
        to_usd(Decimal("100"), "XYZ")

    assert error.value.currency == "XYZ"
