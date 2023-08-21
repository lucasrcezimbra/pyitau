import pytest

from pyitau import Itau


@pytest.fixture
def itau():
    agency = '0000'
    account = '12345'
    account_digit = '6'
    password = '123456'
    return Itau(agency, account, account_digit, password)


@pytest.fixture
def response_authenticate2():
    with open('./tests/responses/authenticate2.html') as file:
        body = file.read()
    return body


@pytest.fixture
def response_authenticate5():
    with open('./tests/responses/authenticate5.html') as file:
        body = file.read()
    return body


@pytest.fixture
def response_authenticate8():
    with open('./tests/responses/authenticate8.html') as file:
        body = file.read()
    return body


@pytest.fixture
def response_menu():
    with open('./tests/responses/menu.html') as file:
        body = file.read()
    return body


@pytest.fixture
def response_cards_page():
    with open('./tests/responses/cards_page.html') as f:
        return f.read()


@pytest.fixture
def response_card_details():
    with open('./tests/responses/card_details.html') as f:
        return f.read()


@pytest.fixture
def response_authenticated_home():
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
def response_checking_account_menu():
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
def response_checking_statements():
    return """
        <div class="botoes clear clearfix no-margem-baixo">
            <a
                id="VerExtrato"
                role="button"
                class="itau-button right"
                onclick="GA.pushModuloCategoria('contaCorrente', 'boxHome', 'verExtrato'); "
                href="javascript:;"
                data-op="PYITAU_OP_statements_by_period"
            >
                <span>ver extrato</span>
            </a>
        </div>
    """


@pytest.fixture
def response_checking_full_statement():
    with open('./tests/responses/checking_account_full_statement.html') as file:
        body = file.read()
    return body


@pytest.fixture
def response_third_router_page():
    with open('./tests/responses/third_router_page.html') as f:
        return f.read()
