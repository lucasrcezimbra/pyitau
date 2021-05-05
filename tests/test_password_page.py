import pytest
from bs4 import BeautifulSoup

from pyitau.pages import PasswordPage


@pytest.fixture
def page(response_authenticate8):
    return PasswordPage(response_authenticate8)


def test_init(response_authenticate8):
    page = PasswordPage(response_authenticate8)
    assert page._soup == BeautifulSoup(response_authenticate8, features='html.parser')


def test_get_keys(page):
    keys = page._get_keys()
    assert len(keys) == 5
    assert keys == page._soup.find(class_='teclado').find(class_='teclas').findAll(class_='campoTeclado')


def test_password_mapper(page):
    page = PasswordPage(
        """
<div class="teclado clearfix">
    <div class="teclas clearfix">
        <a href="javascript:;" aria-label="1 ou 2" rel="tecla_L" class="tecla left campoTeclado" role="button" >1 ou 2</a>
        <a href="javascript:;" aria-label="3 ou 4" rel="tecla_U" class="tecla left campoTeclado" role="button" >3 ou 4</a>
        <a href="javascript:;" aria-label="5 ou 6" rel="tecla_C" class="tecla left campoTeclado" role="button" >5 ou 6</a>
        <a href="javascript:;" aria-label="7 ou 8" rel="tecla_A" class="tecla left campoTeclado" role="button" >7 ou 8</a>
        <a href="javascript:;" aria-label="9 ou 0" rel="tecla_S" class="tecla left campoTeclado" role="button" >9 ou 0</a>
    </div>
</div>
        """
    )
    assert page._get_password_mapper() == {
        '1': 'L',
        '2': 'L',
        '3': 'U',
        '4': 'U',
        '5': 'C',
        '6': 'C',
        '7': 'A',
        '8': 'A',
        '9': 'S',
        '0': 'S',
    }


def test_letter_password(page):
    page = PasswordPage(
        """
<div class="teclado clearfix">
    <div class="teclas clearfix">
        <a href="javascript:;" aria-label="1 ou 2" rel="tecla_L" class="tecla left campoTeclado" role="button" >1 ou 2</a>
        <a href="javascript:;" aria-label="3 ou 4" rel="tecla_U" class="tecla left campoTeclado" role="button" >3 ou 4</a>
        <a href="javascript:;" aria-label="5 ou 6" rel="tecla_C" class="tecla left campoTeclado" role="button" >5 ou 6</a>
        <a href="javascript:;" aria-label="7 ou 8" rel="tecla_A" class="tecla left campoTeclado" role="button" >7 ou 8</a>
        <a href="javascript:;" aria-label="9 ou 0" rel="tecla_S" class="tecla left campoTeclado" role="button" >9 ou 0</a>
    </div>
</div>
        """
    )
    assert page.letter_password('123456') == 'LLUUCC'
    assert page.letter_password('135790') == 'LUCASS'
    assert page.letter_password('097531') == 'SSACUL'


def test_op(page):
    assert page.op == 'PYITAU_OP8'
