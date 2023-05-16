import re

from bs4 import BeautifulSoup


class TextPage:
    def __init__(self, response_text):
        self._text = response_text

    def __eq__(self, other):
        return self._text == other._text


class SoupPage(TextPage):
    def __init__(self, response_text):
        super().__init__(response_text)
        self._soup = BeautifulSoup(self._text, features='html.parser')


class FirstRouterPage(TextPage):
    """
    Primeira página após enviar o formulário de Agência e Conta.
    Utilizada para extrair do HTML informações que serão necessárias nas
    próximas requisições.
    """
    @property
    def auth_token(self):
        """
        Token de autenticação utilizado como cookie nas próximas requisições
        """
        return re.search("authToken=\\'(.*?)\\';", self._text).group(1)

    @property
    def client_id(self):
        return re.search(r"var clientId=\'(.*?)\';", self._text).group(1)

    @property
    def flow_id(self):
        return re.search("var flowId=\'(.*)\';", self._text).group(1)

    @property
    def secapdk(self):
        return re.search(r"\$SECAPDK[\n\r\t\s]*.uidap\(\'(.*?)\'\);", self._text).group(1)

    @property
    def secbcatch(self):
        return re.search(r"\$SECBCATCH[\n\r\t\s]*.uidap\(\'(.*)\'\);", self._text).group(1)

    @property
    def perform_request(self):
        pattern = r'router[\n\r\t\s]*.performRequest\([\n\r\t\s]*"(.*?)",'
        return re.search(pattern, self._text).group(1)


class SecondRouterPage(TextPage):
    """
    Segunda página após enviar o formulário de Agência e Conta.
    Também utilizada para extrair do HTML informações que serão necessárias nas
    próximas requisições.
    """
    @property
    def op_sign_command(self):
        return re.search('__opSignCommand = "(.*?)";', self._text).group(1)

    @property
    def op_maquina_pirata(self):
        return re.search('__opMaquinaPirata = "(.*?)";', self._text).group(1)

    @property
    def guardiao_cb(self):
        return re.search(
            r'var guardiao_cb = function\(\) {\n\t\t\tloadPage\(\'(.*?)\'\);',
            self._text
        ).group(1)


class PasswordPage(SoupPage):
    """
    Página do teclado da senha. Contém 2 dígitos por botão.
    Por baixo dos panos cada botão representa uma letra.
    A combinação das letras deve ser enviada na próxima requisição.
    """
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


class AuthenticatedHomePage(SoupPage):
    """
    Primeira página após o login
    """
    @property
    def op(self):
        return self._soup.find('div', class_='logo left').find('a').attrs['data-op']


class MenuPage(TextPage):
    @property
    def checking_account_op(self):
        return re.search(
            'urlBox : "(.*?)".*seletorContainer : "#boxContaCorrente",',
            self._text,
            flags=re.DOTALL,
        ).group(1)

    @property
    def checking_cards_op(self):
        return re.search(
            r'urlBox : "([^"]+)"[\n\t\r\s,]*seletorContainer : "#boxCartoes",',
            self._text,
            flags=re.DOTALL,
        ).group(1)


class BiggerMenuPage(TextPage):
    """Page that contains the big menu with all the possible account options."""

    @property
    def checking_cards_home_op(self):
        return re.search(
            r"'cartoes','homeCategoria'(.*?)\"[\n\r\s\t]+data-op=\'([^\']+)\'",
            self._text,
            flags=re.DOTALL,
        ).group(2)

    @property
    def checking_cards_op(self):
        return re.search(
            r"'cartoes','cartoes/faturaLimite'(.*?)\""
            r"[\n\r\s\t]+data-op=\'([^\']+)\'",
            self._text,
            flags=re.DOTALL,
        ).group(2)

    @property
    def pix_statements_op(self):
        return re.search(
            r"'pix','pix/extratoPix'(.*?)[\n\t\r\s]data-op='([^\"]+)'",
            self._text,
            flags=re.DOTALL,
        ).group(2)


class CheckingAccountMenu(TextPage):
    @property
    def statements_op(self):
        return re.search(
            'urlBox : "(.*?)".*seletorContainer : ".conteudoBoxContaCorrente",',
            self._text,
            flags=re.DOTALL,
        ).group(1)


class CheckingCardsMenu(TextPage):
    @property
    def cards_op(self):
        return re.search(
            r'urlBox : \'([^\']+)\'[\n\r\t\s,]*seletorContainer : "\.conteudoBoxCartoes",',
            self._text,
            flags=re.DOTALL,
        ).group(1)


class CheckingAccountStatementsPage(SoupPage):
    @property
    def full_statement_op(self):
        return self._soup.find('a').attrs['data-op']


class CardsPage(SoupPage):
    @property
    def card_details_op(self):
        form_invoice = self._soup.find('form', id='formVerFaturaRedesenho')
        return form_invoice.find('input', {'name': 'op'}).attrs['data-op']

    @property
    def first_card_id(self):
        form_invoice = self._soup.find('form', id='formVerFaturaRedesenho')
        return form_invoice.find('input', {'name': 'idCartao'}).attrs['value']


class CheckingAccountFullStatement(TextPage):
    @property
    def filter_statements_by_period_op(self):
        pattern = 'function consultarLancamentosPorPeriodo.*' \
                  '"periodoConsulta" : parametrosPeriodo.*?' \
                  'url = "(.*?)";'
        return re.search(pattern, self._text, flags=re.DOTALL).group(1)

    @property
    def filter_statements_by_month_op(self):
        pattern = 'function consultarLancamentosPorPeriodo.*' \
                  '"mesCompleto" : parametrosPeriodo.*?' \
                  'url = "(.*?)";'
        return re.search(pattern, self._text, flags=re.DOTALL).group(1)


class CardDetails(TextPage):
    @property
    def full_invoice_op(self):
        return re.search(
            r'if \(habilitaFaturaCotacaoDolar === "true"\) '
            r'{[\n\t\r\s]+urlContingencia = "([^"]+)"',
            self._text,
            flags=re.DOTALL,
        ).group(1)


class PixPage(SoupPage):
    @property
    def pix_statements_op(self):
        return re.search(
            r"self.consultarLancamentos = function\("
            r"periodo, pagina, filtro, ordenacao\){[\n\r\t\s]+"
            r"self.erroApiLancamento = false;[\n\r\t\s]+"
            r"\$.Ajax\({[\n\r\t\s]+"
            r'dataType : "json"[\n\r\t\s,]+'
            r'method : "POST"[\n\r\t\s,]+'
            r"headers : {[\n\r\t\s]+"
            r'"op" : "([^"]+)"[\n\r\t\s,]+',
            self._text,
            flags=re.DOTALL,
        ).group(1)

    @property
    def pix_future_op(self):
        return re.search(
            r"self.consultarLancamentosFuturos = function\(pagina, ordenacao\){[\n\r\t\s]+"
            r"\$.Ajax\({[\n\r\t\s]+"
            r'dataType : "json"[\n\r\t\s,]+'
            r'method : "POST"[\n\r\t\s,]+'
            r"headers : {[\n\r\t\s]+"
            r'"op" : "([^"]+)"[\n\r\t\s,]+',
            self._text,
            flags=re.DOTALL,
        )

    @property
    def pix_impressao_html_op(self):
        return re.search(
            r"imprimirTemplateHTML\([\n\r\t\s]+"
            r"'Detalhes',[\n\r\t\s]"
            r"+null,[\n\r\t\s]+"
            r"'([^']+)'",
            self._text,
            flags=re.DOTALL,
        ).group(1)

    @property
    def pix_impressao_op(self):
        form = self._soup.find("form", attrs={"id": "formImpressaoPDF"})
        input = form.find("input", {"name": "op", "type": "hidden"})
        return input.attrs["data-op"]
