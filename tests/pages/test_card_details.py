from pyitau.pages import CardDetails


def test_init(response_card_details: str):
    card_details = CardDetails(response_card_details)
    assert card_details._text == response_card_details


def test_op(response_card_details: str):
    card_details = CardDetails(response_card_details)
    assert card_details.full_invoice_op == 'PYITAU_URL_CONTIGENCIA_DOLAR_OP'
