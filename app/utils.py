from app.consts import MIN_POKEMON_ID, MAX_POKEMON_ID
from app.errors import InvalidValueType, ValueTooBig, ValueTooSmall


def check_if_int(value: float) -> int:
    if value.is_integer():
        return int(value)
    raise InvalidValueType("Number must be integer, not float")


def check_if_float(value: [float, str, int]) -> float:
    try:
        return float(value)
    except ValueError as e:
        raise InvalidValueType(f"Number must be integer: {e}")


def check_range(value: int):
    if value > MAX_POKEMON_ID:
        raise ValueTooBig(f"Value must be smaller than 898, provided {value}")
    elif value < MIN_POKEMON_ID:
        raise ValueTooSmall(f"Value must be bigger than 0, provided {value}")
