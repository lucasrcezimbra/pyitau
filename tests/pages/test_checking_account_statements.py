import pytest
from bs4 import BeautifulSoup

from pyitau.pages import CheckingAccountStatements


@pytest.fixture
def page(response_checking_statements):
    return CheckingAccountStatements(response_checking_statements)


def test_init(response_checking_statements):
    page = CheckingAccountStatements(response_checking_statements)
    assert page._soup == BeautifulSoup(
        response_checking_statements, features="html.parser"
    )


def test_statements_op(page):
    assert page.full_statement_op == "PYITAU_OP_statements_by_period"
