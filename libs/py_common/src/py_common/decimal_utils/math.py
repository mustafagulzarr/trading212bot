from decimal import Decimal, ROUND_HALF_UP

MONEY_QUANT = Decimal("0.00000001")


def to_decimal(value: str | int | float | Decimal) -> Decimal:
    return Decimal(str(value))


def quantize_money(value: Decimal) -> Decimal:
    return value.quantize(MONEY_QUANT, rounding=ROUND_HALF_UP)
