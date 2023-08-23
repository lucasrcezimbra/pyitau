import pytest

from pyitau.pages import CheckingAccountFullStatement


@pytest.fixture
def page(response_checking_full_statement):
    return CheckingAccountFullStatement(response_checking_full_statement)


def test_period_op(page):
    assert page.filter_statements_by_period_op == "PYITAU_OP_PERIOD_filter_statements=;"


def test_month_op(page):
    assert page.filter_statements_by_month_op == "PYITAU_OP_MONTH_filter_statements=;"
