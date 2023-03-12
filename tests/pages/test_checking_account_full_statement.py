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


def test_period_op(page):
    assert page.filter_statements_by_period_op == 'PYITAU_OP_PERIOD_filter_statements=;'


def test_month_op(page):
    assert page.filter_statements_by_month_op == 'PYITAU_OP_MONTH_filter_statements=;'
