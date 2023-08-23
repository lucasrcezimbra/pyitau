import pytest
import requests
import responses

from pyitau.main import ROUTER_URL, Itau
from pyitau.pages import (
    AuthenticatedHome,
    CheckingAccountFullStatement,
    CheckingAccountMenu,
    CheckingAccountStatements,
    Menu,
)


@pytest.fixture
def itau():
    return Itau("0000", "12345", "6", "123456")


@pytest.fixture
def authenticated_home_page(response_authenticated_home):
    return AuthenticatedHome(response_authenticated_home)


@pytest.fixture
def menu_page(response_menu):
    return Menu(response_menu)


@pytest.fixture
def checking_menu_page(response_checking_account_menu):
    return CheckingAccountMenu(response_checking_account_menu)


@pytest.fixture
def checking_statements_page(response_checking_statements):
    return CheckingAccountStatements(response_checking_statements)


def test_init():
    agency = "0000"
    account = "12345"
    account_digit = "6"
    password = "123456"

    itau = Itau(agency, account, account_digit, password)

    assert itau.agency == agency
    assert itau.account == account
    assert itau.account_digit == account_digit
    assert itau.password == password
    assert isinstance(itau._session, requests.Session)


@responses.activate
def test_menu_page(authenticated_home_page, itau, response_menu):
    itau._home = authenticated_home_page
    request1 = responses.post(
        ROUTER_URL,
        body="",
        match=[
            responses.matchers.header_matcher(
                {"op": authenticated_home_page.op, "segmento": "VAREJO"}
            )
        ],
    )
    request2 = responses.post(
        ROUTER_URL,
        body=response_menu,
        match=[
            responses.matchers.header_matcher({"op": authenticated_home_page.menu_op})
        ],
    )

    assert itau._menu_page == Menu(response_menu)
    assert itau._menu_page == Menu(response_menu)

    assert request1.call_count == 1
    assert request2.call_count == 1


@responses.activate
def test_checking_menu_page(menu_page, itau, response_checking_account_menu):
    itau._menu_page = menu_page

    request = responses.post(
        ROUTER_URL,
        body=response_checking_account_menu,
        match=[
            responses.matchers.header_matcher({"op": menu_page.checking_account_op})
        ],
    )

    assert itau._checking_menu_page == CheckingAccountMenu(
        response_checking_account_menu
    )
    assert itau._checking_menu_page == CheckingAccountMenu(
        response_checking_account_menu
    )

    assert request.call_count == 1


@responses.activate
def test_checking_statements_page(
    checking_menu_page, itau, response_checking_statements
):
    itau._checking_menu_page = checking_menu_page

    request = responses.post(
        ROUTER_URL,
        body=response_checking_statements,
        match=[
            responses.matchers.header_matcher({"op": checking_menu_page.statements_op})
        ],
    )

    expected_page = CheckingAccountStatements(response_checking_statements)

    assert itau._checking_statements_page == expected_page
    assert itau._checking_statements_page == expected_page

    assert request.call_count == 1


@responses.activate
def test_checking_full_statement_page(
    checking_statements_page, itau, response_checking_full_statement
):
    itau._checking_statements_page = checking_statements_page

    request = responses.post(
        ROUTER_URL,
        body=response_checking_full_statement,
        match=[
            responses.matchers.header_matcher(
                {"op": checking_statements_page.full_statement_op}
            )
        ],
    )

    expected_page = CheckingAccountFullStatement(response_checking_full_statement)

    assert itau._checking_full_statement_page == expected_page
    assert itau._checking_full_statement_page == expected_page

    assert request.call_count == 1
