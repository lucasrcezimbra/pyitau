import pytest

from pyitau.pages import Menu2Page


@pytest.fixture
def response(response_menu2):
    return response_menu2


@pytest.fixture
def page(response):
    return Menu2Page(response)


def test_init(response):
    page = Menu2Page(response)
    assert page._text == response


def test_checking_cards_op(page):
    assert page.checking_cards_op == 'PYITAU_OP_cartoes'
