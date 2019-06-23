import pytest

from itau import Itau


@pytest.fixture
def itau():
    agency = '0000'
    account = '12345'
    account_digit = '6'
    password = '123456'
    return Itau(agency, account, account_digit, password)
