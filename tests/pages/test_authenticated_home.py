import pytest
from bs4 import BeautifulSoup

from pyitau.pages import AuthenticatedHomePage


@pytest.fixture
def response():
    return """
        <div class="logo left">
            <a
               data-op="PYITAU_OP"
               href=""
               id="HomeLogo"
               onclick="GA.pushHeader('logoItau');"
               title="Home"
            >
                <img
                    alt="Logo Itaú"
                    height="50"
                    src="https://estatico.itau.com.br/.../logo-itau.png"
                    width="50"
                />
            </a>
        </div>
    """


@pytest.fixture
def page(response):
    return AuthenticatedHomePage(response)


def test_init(response):
    page = AuthenticatedHomePage(response)
    assert page._soup == BeautifulSoup(response, features='html.parser')


def test_op(page):
    assert page.op == 'PYITAU_OP'
