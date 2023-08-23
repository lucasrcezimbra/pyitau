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
        self._soup = BeautifulSoup(self._text, features="html.parser")


class FirstRouter(TextPage):
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
        return re.search(r"authToken=\'(.*?)\';", self._text).group(1)

    @property
    def client_id(self):
        return re.search(r"var clientId=\'(.*?)\';", self._text).group(1)

    @property
    def flow_id(self):
        return re.search(r"var flowId='(.*)';", self._text).group(1)

    @property
    def secapdk(self):
        return re.search(r"\$SECAPDK[\n\r\t\s]*.uidap\(\'(.*?)\'\);", self._text).group(
            1
        )

    @property
    def secbcatch(self):
        return re.search(
            r"\$SECBCATCH[\n\r\t\s]*.uidap\(\'(.*)\'\);", self._text
        ).group(1)

    @property
    def perform_request(self):
        pattern = r'router[\n\r\t\s]*.performRequest\([\n\r\t\s]*"(.*?)",'
        return re.search(pattern, self._text).group(1)


class SecondRouter(TextPage):
    """
    Segunda página após enviar o formulário de Agência e Conta.
    Também utilizada para extrair do HTML informações que serão necessárias nas
    próximas requisições.
    """

    @property
    def op_sign_command(self):
        return re.search(r'__opSignCommand = "(.*?)";', self._text).group(1)

    @property
    def op_maquina_pirata(self):
        return re.search(r'__opMaquinaPirata = "(.*?)";', self._text).group(1)

    @property
    def guardiao_cb(self):
        return re.search(
            r"var guardiao_cb = function\(\) {\n\t\t\tloadPage\(\'(.*?)\'\);",
            self._text,
        ).group(1)


class ThirdRouter(SoupPage):
    """
    Página com escolha do titular caso a conta tenha mais de um titular.
    """

    @property
    def op(self):
        """
        Campo op do formulário de titularidade
        """
        return self._soup.find("input", id="op").attrs["value"]

    @property
    def has_account_holders_form(self):
        return bool(self._soup.find("form", attrs={"id": "formTitularidade"}))

    @property
    def account_holders(self):
        form = self._soup.find("form", attrs={"id": "formTitularidade"})
        ul = form.find(name="ul", attrs={"class": "selecao-nome-titular"})
        atags = ul.find_all(
            "a", attrs={"href": re.compile("javascript:titularSelecionado")}
        )
        return [
            re.search(
                r"javascript:titularSelecionado\('(\w+)', '(\d)'\);", tag.attrs["href"]
            ).groups()
            for tag in atags
        ]

    def find_account_holder(self, holder_name):
        for name, id in self.account_holders:
            if name != holder_name:
                continue
            return (name, id)


class Password(SoupPage):
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
        return self._soup.find("input", id="op").attrs["value"]

    def _get_keys(self):
        """
        Retorna lista de elementos HTML A que representam os botões que compõem
        o teclado da senha. Cada botão tem 2 dígitos e é representado por 1 letra.
        Dígitos e letras mudam a cada tentativa de login.
        """
        div_teclado = self._soup.find(class_="teclado")
        div_teclas = div_teclado.find(class_="teclas")
        return div_teclas.findAll(class_="campoTeclado")

    def _get_password_mapper(self):
        """
        Retorna de/para do número para letra da senha
        """
        mapper = {}

        for key in self._get_keys():
            numbers = key.attrs["aria-label"].split(" ou ")
            letter = key.attrs["rel"][0].replace("tecla_", "")
            mapper[numbers[0]] = letter
            mapper[numbers[1]] = letter

        return mapper

    def letter_password(self, password):
        """
        Recebe senha de número e retorna em letras do teclado da senha.
        """
        mapper = self._get_password_mapper()
        return "".join(mapper[n] for n in password)


class AuthenticatedHome(SoupPage):
    """
    Primeira página após o login
    """

    @property
    def op(self):
        return self._soup.find("div", class_="logo left").find("a").attrs["data-op"]

    @property
    def menu_op(self):
        return re.search(
            r"var obterMenu = function\(\) \{"
            r'[\n\t\r\s]+var perfil = \$\("#portalTxt"\).val\(\);'
            r"[\n\t\r\s]+\$.ajax\(\{"
            r'[\n\t\r\s]+url : "([^"]+)"',
            self._text,
            flags=re.DOTALL,
        ).group(1)


class Menu(TextPage):
    @property
    def checking_cards_op(self):
        return re.search(
            r"'cartoes','homeCategoria'(.*?)\"[\n\r\s\t]+data-op=\'([^\']+)\'",
            self._text,
            flags=re.DOTALL,
        ).group(2)

    @property
    def checking_account_op(self):
        return re.search(
            r"'contaCorrente','homeCategoria'(.*?)\"[\n\r\s\t]+data-op=\'([^\']+)\'",
            self._text,
            flags=re.DOTALL,
        ).group(2)


class CheckingAccountMenu(TextPage):
    @property
    def statements_op(self):
        return re.search(r'url : "(.*)"', self._text).group(1)


class CheckingCardsMenu(TextPage):
    @property
    def cards_op(self):
        return re.search(
            r'urlBox : \'([^\']+)\'[\n\r\t\s,]*seletorContainer : "\.conteudoBoxCartoes",',
            self._text,
            flags=re.DOTALL,
        ).group(1)


class CheckingAccountStatements(SoupPage):
    @property
    def full_statement_op(self):
        return self._soup.find("a").attrs["data-op"]


class Cards(SoupPage):
    @property
    def card_details_op(self):
        form_invoice = self._soup.find("form", id="formVerFaturaRedesenho")
        return form_invoice.find("input", {"name": "op"}).attrs["data-op"]

    @property
    def first_card_id(self):
        form_invoice = self._soup.find("form", id="formVerFaturaRedesenho")
        return form_invoice.find("input", {"name": "idCartao"}).attrs["value"]


class CheckingAccountFullStatement(TextPage):
    @property
    def filter_statements_by_period_op(self):
        pattern = (
            r"function consultarLancamentosPorPeriodo.*"
            r'"periodoConsulta" : parametrosPeriodo.*?'
            r'url = "(.*?)";'
        )
        return re.search(pattern, self._text, flags=re.DOTALL).group(1)

    @property
    def filter_statements_by_month_op(self):
        pattern = (
            r"function consultarLancamentosPorPeriodo.*"
            r'"mesCompleto" : parametrosPeriodo.*?'
            r'url = "(.*?)";'
        )
        return re.search(pattern, self._text, flags=re.DOTALL).group(1)


class CardDetails(TextPage):
    @property
    def invoice_op(self):
        try:
            return re.search(
                r'if \(habilitaFaturaCotacaoDolar === "true"\) '
                r'{[\n\t\r\s]+urlContingencia = "([^"]+)"',
                self._text,
                flags=re.DOTALL,
            ).group(1)
        except AttributeError:
            return re.search(
                r'if \(habilitaDashboardCotacaoDolar === "true"\) '
                r'{[\n\t\r\s]+urlContingencia = "([^"]+)"',
                self._text,
                flags=re.DOTALL,
            ).group(1)

    @property
    def full_statement_op(self):
        return re.search(
            r"data: cartaoSelecionado.id," r'[\n\t\r\s]+url: "([^"]+)"',
            self._text,
            flags=re.DOTALL,
        ).group(1)
