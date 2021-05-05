import responses
from bs4 import BeautifulSoup

from pyitau.pages import HomePage


def test_init(response_authenticate0):
    page = HomePage(response_authenticate0)
    assert page._soup == BeautifulSoup(response_authenticate0, features='html.parser')


def test_id(response_authenticate0):
    page = HomePage(response_authenticate0)
    assert page.id == 'PYITAU_ID_VALUE'


def test_op(response_authenticate0):
    page = HomePage(response_authenticate0)
    assert page.op == 'PYITAU_OP1_VALUE'
