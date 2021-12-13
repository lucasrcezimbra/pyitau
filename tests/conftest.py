import pytest

from pyitau import Itau


@pytest.fixture
def itau():
    agency = '0000'
    account = '12345'
    account_digit = '6'
    password = '123456'
    return Itau(agency, account, account_digit, password)


@pytest.fixture
def response_authenticate2():
    with open('./tests/responses/authenticate2.html') as file:
        body = file.read()
    return body


@pytest.fixture
def response_authenticate5():
    with open('./tests/responses/authenticate5.html') as file:
        body = file.read()
    return body


@pytest.fixture
def response_authenticate8():
    with open('./tests/responses/authenticate8.html') as file:
        body = file.read()
    return body
