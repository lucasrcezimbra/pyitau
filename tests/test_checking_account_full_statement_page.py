import pytest

from pyitau.pages import CheckingAccountFullStatement


@pytest.fixture
def response():
    with open('./tests/responses/checking_account_full_statement.html') as file:
        body = file.read()
    return body


@pytest.fixture
def page(response):
    return CheckingAccountFullStatement(response)


def test_op(page):
    assert page.filter_statements_op == 'PYITAU_OP_filter_statements=;'
