import pytest
from bs4 import BeautifulSoup

from pyitau.pages import SecondRouterPage


@pytest.fixture
def page(response_authenticate5):
    return SecondRouterPage(response_authenticate5)


def test_init(response_authenticate5):
    page = SecondRouterPage(response_authenticate5)
    assert page._text == response_authenticate5


def test_op_sign_command(page):
    assert page.op_sign_command == 'PYITAU_OP5'


def test_op_maquina_pirata(page):
    assert page.op_maquina_pirata == 'PYITAU_OP6'


def test_guardiao_cb(page):
    assert page.guardiao_cb == 'PYITAU_OP7'
