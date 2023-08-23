import pytest

from pyitau.pages import MenuPage


@pytest.fixture
def page(response_menu):
    return MenuPage(response_menu)


def test_init(response_menu):
    page = MenuPage(response_menu)
    assert page._text == response_menu


def test_checking_cards_op(page):
    assert page.checking_cards_op == "PYITAU_OP_cartoes"


def test_checking_account_op(page):
    assert page.checking_account_op == "PYITAU_OP_conta_corrente"
