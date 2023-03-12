import requests
from cached_property import cached_property

from pyitau.pages import (AuthenticatedHomePage, CardDetails, CardsPage,
                          CheckingAccountFullStatement, CheckingAccountMenu,
                          CheckingAccountStatementsPage, CheckingCardsMenu,
                          FirstRouterPage, MenuPage, PasswordPage,
                          SecondRouterPage)

ROUTER_URL = 'https://internetpf5.itau.com.br/router-app/router'


class Itau:
    def __init__(self, agency, account, account_digit, password):
        self.agency = agency
        self.account = account
        self.account_digit = account_digit
        self.password = password
        self._session = requests.Session()
        self._session.headers = {
            **self._session.headers,
            'User-Agent': (
                'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 '
                '(KHTML, like Gecko) Ubuntu Chromium/72.0.3626.121 '
                'Chrome/72.0.3626.121 Safari/537.36'
            ),
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
        """
        Get and return the credit card invoice.
        """
        response = self._session.post(
            ROUTER_URL,
            headers={'op': self._menu_page.checking_cards_op}
        )

        cards_menu = CheckingCardsMenu(response.text)
        response = self._session.post(ROUTER_URL, headers={'op': cards_menu.cards_op})

        cards_page = CardsPage(response.text)
        response = self._session.post(ROUTER_URL, headers={'op': cards_page.card_details_op},
                                      data={'idCartao': cards_page.first_card_id})

        card_details = CardDetails(response.text)
        response = self._session.post(ROUTER_URL, headers={'op': card_details.full_invoice_op},
                                      data={'secao': 'Cartoes:MinhaFatura',
                                            'item': ''})
        return response.json()

    def get_statements(self, days=90):
        """
        Get and return the statements of the last days.
        """

        response = self._session.post(
            ROUTER_URL,
            data={'periodoConsulta': days},
            headers={'op': self._checking_full_statement_page.filter_statements_by_period_op},
        )
        return response.json()

    def get_statements_from_month(self, month=1, year=2001):
        """
        Get and return the full statements of a specific month.
        """
        if year < 2001:
            raise Exception(f"Invalid year {year}.")

        if month < 1 or month > 12:
            raise Exception(f"Invalid month {month}.")

        response = self._session.post(
            ROUTER_URL,
            data={'mesCompleto': "%02d/%d" % (month, year)},
            headers={'op': self._checking_full_statement_page.filter_statements_by_month_op},
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

    @cached_property
    def _menu_page(self):
        headers = {'op': self._home.op, 'segmento': 'VAREJO'}
        response = self._session.post(ROUTER_URL, headers=headers)
        return MenuPage(response.text)

    @cached_property
    def _checking_menu_page(self):
        response = self._session.post(
            ROUTER_URL,
            headers={'op': self._menu_page.checking_account_op}
        )
        return CheckingAccountMenu(response.text)

    @cached_property
    def _checking_statements_page(self):
        response = self._session.post(
            ROUTER_URL,
            headers={'op': self._checking_menu_page.statements_op}
        )
        return CheckingAccountStatementsPage(response.text)

    @cached_property
    def _checking_full_statement_page(self):
        response = self._session.post(
            ROUTER_URL,
            headers={'op': self._checking_statements_page.full_statement_op},
        )
        return CheckingAccountFullStatement(response.text)
