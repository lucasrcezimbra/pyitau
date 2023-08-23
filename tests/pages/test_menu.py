import pytest

from pyitau.pages import Menu


@pytest.fixture
def page(response_menu):
    return Menu(response_menu)


def test_init(response_menu):
    page = Menu(response_menu)
    assert page._text == response_menu


def test_checking_cards_op(page):
    assert page.checking_cards_op == "PYITAU_OP_cartoes"


def test_checking_account_op(page):
    assert page.checking_account_op == "PYITAU_OP_conta_corrente"
