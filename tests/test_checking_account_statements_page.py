import pytest
from bs4 import BeautifulSoup

from pyitau.pages import CheckingAccountStatementsPage


@pytest.fixture
def response():
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
def page(response):
    return CheckingAccountStatementsPage(response)


def test_init(response):
    page = CheckingAccountStatementsPage(response)
    assert page._soup == BeautifulSoup(response, features='html.parser')


def test_statements_op(page):
    assert page.full_statement_op == 'PYITAU_OP_statements_by_period'
