import pytest

from pyitau.pages import CardsPage


@pytest.fixture()
def cards_page(response_cards_page: str) -> CardsPage:
    return CardsPage(response_cards_page)


def test_init(response_cards_page: str):
    cards_page = CardsPage(response_cards_page)
    assert cards_page._text == response_cards_page


def test_card_id(cards_page: CardsPage):
    assert cards_page.first_card_id == 'PYITAU_CARD_ID'


def test_card_op(cards_page: CardsPage):
    assert cards_page.card_details_op == 'PYITAU_FATURA_REDESENHO_OP'
