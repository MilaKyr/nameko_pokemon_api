import pytest

from app.utils import check_input, check_if_float, check_if_int
from app.errors import ValueTooSmall, ValueTooBig, InvalidValueType


def test_check_input_with_str():
    pytest.raises(InvalidValueType, check_input, "a")


def test_check_if_float_with_float():
    result = check_if_float(1.5)
    assert result == 1.5


def test_check_input_with_float():
    pytest.raises(InvalidValueType, check_input, 1.5)


def test_check_if_int_with_round_float():
    result = check_if_int(1.0)
    assert result == 1.0


def test_range_limit_int_type_fail_with_zero():
    pytest.raises(ValueTooSmall, check_input, 0)


def test_range_limit_int_type_fail_with_negative():
    pytest.raises(ValueTooSmall, check_input, -10)


def test_range_limit_int_type_fail_with_too_high_id():
    pytest.raises(ValueTooBig, check_input, 10_000)


def test_check_input():
    result = check_input(10)
    assert result == 10
