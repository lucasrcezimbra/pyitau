import pytest

from pyitau.pages import CheckingCards


@pytest.fixture()
def response():
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


def test_init(response):
    page = CheckingCards(response)
    assert page._text == response


def test_op(response):
    page = CheckingCards(response)
    assert page.cards_op == "PYITAU_CONTEUDO_BOX_CARTOES_OP"
