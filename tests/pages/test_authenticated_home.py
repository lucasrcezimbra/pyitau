import pytest
from bs4 import BeautifulSoup

from pyitau.pages import AuthenticatedHomePage


@pytest.fixture
def response():
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
def page(response):
    return AuthenticatedHomePage(response)


def test_init(response):
    page = AuthenticatedHomePage(response)
    assert page._soup == BeautifulSoup(response, features='html.parser')


def test_menu_op(page):
    assert page.menu_op == 'PYITAU_MENU_OP'


def test_op(page):
    assert page.op == 'PYITAU_OP'
