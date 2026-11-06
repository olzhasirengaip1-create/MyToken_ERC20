import pytest
from app.blockchain import validate_positive_amount, validate_address

def test_positive_integer_amount():
    assert validate_positive_amount("12") == 12

def test_zero_amount_rejected():
    with pytest.raises(ValueError):
        validate_positive_amount("0")

def test_negative_amount_rejected():
    with pytest.raises(ValueError):
        validate_positive_amount("-4")

def test_fractional_amount_rejected():
    with pytest.raises(ValueError):
        validate_positive_amount("1.5")

def test_invalid_address_rejected():
    with pytest.raises(ValueError):
        validate_address("not-an-ethereum-address")
