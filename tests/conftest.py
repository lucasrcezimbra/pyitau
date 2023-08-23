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
        <input type="hidden" id="portalTxt" value="varejo"/>
        <script id="item" type="text/javascript">
            var obterMenu = function() {
                var perfil = $("#portalTxt").val();
                $.ajax({
                    url : "PYITAU_MENU_OP",
                    dataType : "html",
                    method : "POST",
                    async: true,
                    showLoading: false,
                    headers : {
                        "ajaxRequest" : true
                    },
                    success : function(data) {
                        $("#menu_p_fisica").replaceWith(data);

                    },
                    error : function(erro){
                        $("#formError").submit();
                    }
                });
            };

            if(window.addEventListener){
                window.addEventListener('load', obterMenu)
            } else {
                window.attachEvent('onload', obterMenu)
            }
        </script></li>
                    </ul>
                </nav>

                <div class="logo left">
                    <a onclick="GA.pushHeader('logoItau');" href=""
                        title="Home"
                        id="HomeLogo"
                        data-op="PYITAU_OP">


                            <img src="https://estatico.itau.com.br/.../logo-itau.png" width="50"
                                    height="50" alt="Logo Ita&uacute;" />


                    </a>
                </div>
    """


@pytest.fixture
def response_checking_account_menu():
    return """
    <script id='scriptmenuContexto' type="text/javascript">
        var obterMenuContextomenuContexto = function() {
            $(".blockUI").remove();
            $.ajax({
                url : "PYITAU_OP_statement",
                dataType : "html",
                method : "POST",
                showLoading:false,
                data : {
                    "contexto" : "",
                    "montarModulo" : "",
                    "mapaDoSite" : ""
                },
                headers : {
                    "ajaxRequest" : true
                },
                success : function(data) {
                    $('#menuContexto').replaceWith(data);
                    $('html').removeClass("uiConfiguration-runed");
                }
            });
        };

        $(function() {
            obterMenuContextomenuContexto();
        });
    </script>
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
def response_menu():
    return """
        <li class="titulo "  >
            <a onclick="GA.pushMegaMenu('contaCorrente','homeCategoria');disparar('Clique;...');"
                data-op='PYITAU_OP_conta_corrente'
                href="javascript:;"
                tabindex="2"

                >
                conta corrente
            </a>
        </li>

        <li class="titulo "  >
            <a onclick="GA.pushMegaMenu('cartoes','homeCategoria');...;"
                data-op='PYITAU_OP_cartoes'
                href="javascript:;"
                tabindex="24"

                >
                cart&otilde;es
            </a>
        </li>
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
