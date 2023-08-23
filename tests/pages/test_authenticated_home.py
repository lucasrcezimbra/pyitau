import pytest
from bs4 import BeautifulSoup

from pyitau.pages import AuthenticatedHomePage


@pytest.fixture
def response(response_authenticated_home):
    return response_authenticated_home


@pytest.fixture
def page(response):
    return AuthenticatedHomePage(response)


def test_init(response):
    page = AuthenticatedHomePage(response)
    assert page._soup == BeautifulSoup(response, features="html.parser")


def test_menu_op(page):
    assert page.menu_op == "PYITAU_MENU_OP"


def test_op(page):
    assert page.op == "PYITAU_OP"
