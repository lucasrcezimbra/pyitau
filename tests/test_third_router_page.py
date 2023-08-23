import pytest
from bs4 import BeautifulSoup

from pyitau.pages import ThirdRouter


@pytest.fixture
def page(response_third_router_page):
    return ThirdRouter(response_third_router_page)


def test_init(response_third_router_page):
    page = ThirdRouter(response_third_router_page)
    assert page._soup == BeautifulSoup(
        response_third_router_page, features="html.parser"
    )


def test_op(page):
    assert page.op == "PYITAU_OP_THIRD_ROUTER_PAGE"


def test_has_account_holders_form(page):
    assert page.has_account_holders_form is True


def test_account_holders(page):
    assert page.account_holders == [("FULANO", "0"), ("SICLANO", "1")]


def test_find_account_holder(page):
    assert page.find_account_holder("FULANO") == ("FULANO", "0")
    assert page.find_account_holder("SICLANO") == ("SICLANO", "1")
