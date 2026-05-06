from decimal import Decimal

from hypothesis import given
from hypothesis import strategies as st

from py_common.decimal_utils.math import quantize_money, to_decimal


@given(st.decimals(min_value="0", max_value="100000", allow_nan=False, allow_infinity=False, places=10))
def test_quantize_money_precision(value: Decimal) -> None:
    quantized = quantize_money(value)
    assert abs(quantized.as_tuple().exponent) <= 8


def test_to_decimal_strips_float_binary_noise() -> None:
    result = to_decimal(0.1)
    assert result == Decimal("0.1")
