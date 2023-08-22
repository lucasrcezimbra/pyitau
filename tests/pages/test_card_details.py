import pytest

from pyitau.pages import CardDetails


@pytest.fixture
def page(response_card_details):
    return CardDetails(response_card_details)


def test_init(response_card_details):
    card_details = CardDetails(response_card_details)
    assert card_details._text == response_card_details


def test_invoice_op(page):
    assert page.invoice_op == "PYITAU_invoice_op"


def test_full_statement_op(page):
    assert page.full_statement_op == "PYITAU_full_statement_op"
