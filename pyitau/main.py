import requests

from pyitau.pages import (AuthenticatedHomePage, CheckingAccountFullStatement,
                          CheckingAccountMenu, CheckingAccountStatementsPage,
                          FirstRouterPage, MenuPage, PasswordPage,
                          SecondRouterPage)

ROUTER_URL = 'https://internetpf5.itau.com.br/router-app/router'


class Itau:
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 '
                      '(KHTML, like Gecko) Ubuntu Chromium/72.0.3626.121 '
                      'Chrome/72.0.3626.121 Safari/537.36'
    }

    def __init__(self, agency, account, account_digit, password):
        self.agency = agency
        self.account = account
        self.account_digit = account_digit
        self.password = password
        self._session = requests.Session()
        self._session.headers = {
            **self._session.headers,
            **self.headers,
        }

    def authenticate(self):
        self._authenticate2()
        self._authenticate3()
        self._authenticate4()
        self._authenticate5()
        self._authenticate6()
        self._authenticate7()
        self._authenticate8()
        self._authenticate9()

    def get_credit_card_invoice(self):
        op = self._home.find('div', class_='logo left').find('a').attrs['data-op']

        headers = {'op': op, 'segmento': 'VAREJO'}
        response = self._session.post(ROUTER_URL, headers=headers)
        op2 = re.search(
            r'urlBox : "([^"]+)"[\n\t\r\s,]*seletorContainer : "#boxCartoes",',
            response.text,
            flags=re.DOTALL,
        ).group(1)
        print('op2', op2)

        response = self._session.post(ROUTER_URL, headers={'op': op2})

        op3 = re.search(
            r'urlBox : \'([^\']+)\'[\n\r\t\s,]*seletorContainer : "\.conteudoBoxCartoes",',
            response.text,
            flags=re.DOTALL,
        ).group(1)
        response = self._session.post(ROUTER_URL, headers={'op': op3})
        cartoes_page = BeautifulSoup(response.text, features='html.parser')
        form_ver_fatura = cartoes_page.find('form', id='formVerFaturaRedesenho')
        op4 = form_ver_fatura.find('input', {'name': 'op'}).attrs['data-op']
        id_cartao = form_ver_fatura.find('input', {'name': 'idCartao'}).attrs['value']
        response = self._session.post(ROUTER_URL, headers={'op': op4},
                                      data={'idCartao': id_cartao})

        op5 = re.search(
            r'if \(habilitaFaturaCotacaoDolar === "true"\) '
            r'{[\n\t\r\s]+urlContingencia = "([^"]+)"',
            response.text,
            flags=re.DOTALL,
        ).group(1)
        response = self._session.post(ROUTER_URL, headers={'op': op5},
                                      data={'secao': 'Cartoes:MinhaFatura',
                                            'item': ''})
        return response.json()

    def get_statements(self):
        headers = {'op': self._home.op, 'segmento': 'VAREJO'}

        response = self._session.post(ROUTER_URL, headers=headers)
        menu = MenuPage(response.text)

        response = self._session.post(ROUTER_URL, headers={'op': menu.checking_account_op})
        account_menu = CheckingAccountMenu(response.text)

        response = self._session.post(ROUTER_URL, headers={'op': account_menu.statements_op})
        statements_page = CheckingAccountStatementsPage(response.text)

        response = self._session.post(
            ROUTER_URL,
            headers={'op': statements_page.full_statement_op},
        )
        full_statement_page = CheckingAccountFullStatement(response.text)

        response = self._session.post(
            ROUTER_URL,
            data={'periodoConsulta': 90},
            headers={'op': full_statement_page.filter_statements_op},
        )
        return response.json()

    def _authenticate2(self):
        data = {
            'portal': '005',
            'pre-login': 'pre-login',
            'tipoLogon': '7',
            'usuario.agencia': self.agency,
            'usuario.conta': self.account,
            'usuario.dac': self.account_digit,
            'destino': '',
        }
        response = self._session.post(ROUTER_URL, data=data)
        page = FirstRouterPage(response.text)
        self._session.cookies.set('X-AUTH-TOKEN', page.auth_token)
        self._op2 = page.secapdk
        self._op3 = page.secbcatch
        self._op4 = page.perform_request
        self._flow_id = page.flow_id
        self._client_id = page.client_id

    def _authenticate3(self):
        headers = {
            'op': self._op2,
            'X-FLOW-ID': self._flow_id,
            'X-CLIENT-ID': self._client_id,
            'renderType': 'parcialPage',
            'X-Requested-With': 'XMLHttpRequest',
        }

        self._session.post(ROUTER_URL, headers=headers)

    def _authenticate4(self):
        headers = {'op': self._op3}
        self._session.post(ROUTER_URL, headers=headers)

    def _authenticate5(self):
        headers = {'op': self._op4}
        response = self._session.post(ROUTER_URL, headers=headers)
        page = SecondRouterPage(response.text)
        self._op5 = page.op_sign_command
        self._op6 = page.op_maquina_pirata
        self._op7 = page.guardiao_cb

    def _authenticate6(self):
        headers = {'op': self._op5}
        self._session.post(ROUTER_URL, headers=headers)

    def _authenticate7(self):
        headers = {'op': self._op6}
        self._session.post(ROUTER_URL, headers=headers)

    def _authenticate8(self):
        headers = {'op': self._op7}
        response = self._session.post(ROUTER_URL, headers=headers)
        page = PasswordPage(response.text)

        self._op8 = page.op
        self._letter_password = page.letter_password(self.password)

    def _authenticate9(self):
        headers = {'op': self._op8}
        data = {
            'op': self._op8,
            'senha': self._letter_password
        }

        response = self._session.post(ROUTER_URL, headers=headers, data=data)
        self._home = AuthenticatedHomePage(response.text)
