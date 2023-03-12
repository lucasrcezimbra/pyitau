import pytest

from pyitau.pages import CheckingAccountMenu


@pytest.fixture
def response():
    return """
        $(".accordion-box-conta-corrente").itauAccordion();
        function carregarContaCorrente() {
            if($(".btnExibirBoxContaCorrente").hasClass("ajaxRuned")){
                mudarCookieBoxAberto("boxContaCorrente");
                return;
            }
            BoxHelper.renderConteudoBox({
                urlBox : "PYITAU_OP_statement",
                seletorContainer : ".conteudoBoxContaCorrente",
                onComplete : function() {
                    $(".btnExibirBoxContaCorrente").addClass("ajaxRuned");
                    criarCookieBoxAberto("boxContaCorrente");
                }
            });
        }
    """


@pytest.fixture
def page(response):
    return CheckingAccountMenu(response)


def test_init(response):
    page = CheckingAccountMenu(response)
    assert page._text == response


def test_statements_op(page):
    assert page.statements_op == 'PYITAU_OP_statement'
