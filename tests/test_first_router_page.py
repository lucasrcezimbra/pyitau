import pytest
from bs4 import BeautifulSoup

from pyitau.pages import FirstRouterPage


@pytest.fixture
def page(response_authenticate2):
    return FirstRouterPage(response_authenticate2)


def test_init(response_authenticate2):
    page = FirstRouterPage(response_authenticate2)
    assert page._text == response_authenticate2


def test_auth_token(page):
    assert page.auth_token == 'PYITAU_AUTHTOKEN'


def test_client_id(page):
    assert page.client_id == 'PYITAU_CLIENTID'


def test_flow_id(page):
    assert page.flow_id == 'PYITAU_FLOWID'


def test_secapdk(page):
    assert page.secapdk == 'PYITAU_OP2'


def test_secbcatch(page):
    assert page.secbcatch == 'PYITAU_OP3'


def test_perform_request(page):
    assert page.perform_request == 'PYITAU_OP4'
