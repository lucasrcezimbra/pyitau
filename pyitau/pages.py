import re

from bs4 import BeautifulSoup


class HomePage:
    """
    Página inicial do Itaú. Contém formulário com Agência e Conta.
    Utilizada para extrair informações do formulário de login.
    """
    def __init__(self, response_text):
        self._soup = BeautifulSoup(response_text, features='html.parser')

    @property
    def _form(self):
        """
        Formulário de login com os campos Agência e Conta
        """
        return self._soup.find('form', attrs={'name': 'banklineAgConta'})

    @property
    def id(self):
        """
        Campo id do formulário de Agência/Conta
        """
        return self._form.find('input', attrs={'name': 'portal'}).attrs['value']

    @property
    def op(self):
        """
        Campo op do formulário de Agência/Conta
        """
        return self._form.find('input', attrs={'name': 'tipoLogon'}).attrs['value']


class FirstRouterPage:
    """
    Primeira página após enviar o formulário de Agência e Conta.
    Utilizada para extrair do HTML informações que serão necessárias nas
    próximas requisições.
    """
    def __init__(self, response_text):
        self._text = response_text

    @property
    def auth_token(self):
        """
        Token de autenticação utilizado como cookie nas próximas requisições
        """
        return re.search("authToken=\\'(.*?)\\';", self._text).group(1)

    @property
    def client_id(self):
        return re.search("var clientId=\'(.*?)\';", self._text).group(1)

    @property
    def flow_id(self):
        return re.search("var flowId=\'(.*)\';", self._text).group(1)

    @property
    def secapdk(self):
        return re.search("\$SECAPDK.uidap\(\'(.*?)\'\);", self._text).group(1)

    @property
    def secbcatch(self):
        return re.search("\$SECBCATCH.uidap\(\'(.*)\'\);", self._text).group(1)

    @property
    def perform_request(self):
        return re.search('router.performRequest\("(.*?)", ', self._text).group(1)


class SecondRouterPage:
    """
    Segunda página após enviar o formulário de Agência e Conta.
    Também utilizada para extrair do HTML informações que serão necessárias nas
    próximas requisições.
    """
    def __init__(self, response_text):
        self._text = response_text

    @property
    def op_sign_command(self):
        return re.search('__opSignCommand = "(.*?)";', self._text).group(1)

    @property
    def op_maquina_pirata(self):
        return re.search('__opMaquinaPirata = "(.*?)";', self._text).group(1)

    @property
    def guardiao_cb(self):
        return re.search(
            'var guardiao_cb = function\(\) {\n\t\t\tloadPage\(\'(.*?)\'\);',
            self._text
        ).group(1)


class PasswordPage:
    """
    Página do teclado da senha. Contém 2 dígitos por botão.
    Por baixo dos panos cada botão representa uma letra.
    A combinação das letras deve ser enviada na próxima requisição.
    """
    def __init__(self, response_text):
        self._soup = BeautifulSoup(response_text, features='html.parser')

    @property
    def op(self):
        """
        Campo op do formulário de senha
        """
        return self._soup.find('input', id='op').attrs['value']

    def _get_keys(self):
        """
        Retorna lista de elementos HTML A que representam os botões que compõem
        o teclado da senha. Cada botão tem 2 dígitos e é representado por 1 letra.
        Dígitos e letras mudam a cada tentativa de login.
        """
        div_teclado = self._soup.find(class_='teclado')
        div_teclas = div_teclado.find(class_='teclas')
        return div_teclas.findAll(class_='campoTeclado')

    def _get_password_mapper(self):
        """
        Retorna de/para do número para letra da senha
        """
        mapper = {}

        for key in self._get_keys():
            numbers = key.attrs['aria-label'].split(' ou ')
            letter = key.attrs['rel'][0].replace('tecla_', '')
            mapper[numbers[0]] = letter
            mapper[numbers[1]] = letter

        return mapper

    def letter_password(self, password):
        """
        Recebe senha de número e retorna em letras do teclado da senha.
        """
        mapper = self._get_password_mapper()
        return ''.join(mapper[n] for n in password)
