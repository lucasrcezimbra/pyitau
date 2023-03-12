from unittest.mock import call

import pytest
import responses

from pyitau.main import ROUTER_URL
from pyitau.pages import AuthenticatedHomePage


@pytest.fixture
def response_checking_card_menu():
    return """
    <script>
        $(".accordion-box-cartoes").itauAccordion();
        function carregarBoxCartoes() {
            if($(".btnExibirBoxCartoes").hasClass("ajaxRuned")){
                return;
            }

            BoxHelper.renderConteudoBox({
                urlBox : 'PYITAU_CONTEUDO_BOX_CARTOES_OP',
                seletorContainer : ".conteudoBoxCartoes",
                onComplete : function() {
                    $(".btnExibirBoxCartoes").addClass("ajaxRuned");
                }
            });
        }



        function enviarTagueamentoExibirCartoes(){
            adobeDataLayer.pushCustom('itemClicado', 'BTN:PF:Exibir_cartoes');
            adobeDataLayer.pushCustom('events', ['ClickElement']);
            adobeDataLayer.pushRule('customLink');
            adobeDataLayer.sendDataLayer();
        }
    </script>
    """


@pytest.fixture()
def authenticated_home_page(response_authenticated_home):
    return AuthenticatedHomePage(response_authenticated_home)


@responses.activate
def test_get_credit_card_invoice(
    itau,
    mocker,
    authenticated_home_page,
    response_menu,
    response_checking_card_menu,
    response_cards_page,
    response_card_details,
):
    itau._home = authenticated_home_page

    responses.add(
        responses.POST,
        ROUTER_URL,
        body=response_menu,
        match=[
            responses.matchers.header_matcher(
                {"op": authenticated_home_page.op, "segmento": "VAREJO"}
            )
        ],
    )

    responses.add(
        responses.POST,
        ROUTER_URL,
        body=response_checking_card_menu,
        match=[responses.matchers.header_matcher({"op": "PYITAU_OP_Cartoes"})],
    )

    responses.add(
        responses.POST,
        ROUTER_URL,
        body=response_cards_page,
        match=[
            responses.matchers.header_matcher({"op": "PYITAU_CONTEUDO_BOX_CARTOES_OP"})
        ],
    )

    responses.add(
        responses.POST,
        ROUTER_URL,
        body=response_card_details,
        match=[
            responses.matchers.header_matcher({"op": "PYITAU_FATURA_REDESENHO_OP"}),
            responses.matchers.urlencoded_params_matcher(
                {"idCartao": "PYITAU_CARD_ID"}
            ),
        ],
    )

    responses.add(
        responses.POST,
        ROUTER_URL,
        body="""{"success": true}""",
        match=[
            responses.matchers.header_matcher(
                {"op": "PYITAU_URL_CONTIGENCIA_DOLAR_OP"}
            ),
            responses.matchers.urlencoded_params_matcher(
                {"secao": "Cartoes:MinhaFatura"}
            ),
        ],
    )
    post_spy = mocker.spy(itau._session, "post")
    assert itau.get_credit_card_invoice() == {"success": True}

    calls = [
        call(
            ROUTER_URL, headers={"op": authenticated_home_page.op, "segmento": "VAREJO"}
        ),
        call(ROUTER_URL, headers={"op": "PYITAU_OP_Cartoes"}),
        call(ROUTER_URL, headers={"op": "PYITAU_CONTEUDO_BOX_CARTOES_OP"}),
        call(
            ROUTER_URL,
            headers={"op": "PYITAU_FATURA_REDESENHO_OP"},
            data={"idCartao": "PYITAU_CARD_ID"},
        ),
        call(
            ROUTER_URL,
            headers={"op": "PYITAU_URL_CONTIGENCIA_DOLAR_OP"},
            data={"secao": "Cartoes:MinhaFatura", "item": ""},
        ),
    ]
    post_spy.assert_has_calls(calls)
