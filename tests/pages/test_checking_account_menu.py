import pytest

from pyitau.pages import CheckingAccountMenu


@pytest.fixture
def page(response_checking_account_menu):
    return CheckingAccountMenu(response_checking_account_menu)


def test_init(response_checking_account_menu):
    page = CheckingAccountMenu(response_checking_account_menu)
    assert page._text == response_checking_account_menu


def test_statements_op(page):
    assert page.statements_op == "PYITAU_OP_statement"
