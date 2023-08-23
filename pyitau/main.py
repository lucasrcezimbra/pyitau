import requests
from cached_property import cached_property

from pyitau import pages

ROUTER_URL = "https://internetpf5.itau.com.br/router-app/router"


class Itau:
    def __init__(self, agency, account, account_digit, password, holder_name=None):
        self.agency = agency
        self.account = account
        self.account_digit = account_digit
        self.password = password
        self.holder_name = holder_name
        self._session = requests.Session()
        self._session.headers = {
            **self._session.headers,
            "User-Agent": (
                "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
                "(KHTML, like Gecko) Ubuntu Chromium/72.0.3626.121 "
                "Chrome/72.0.3626.121 Safari/537.36"
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

    def get_credit_card_invoice(self, card_name=None):
        """
        Get and return the credit card invoice.
        """
        response = self._session.post(
            ROUTER_URL,
            headers={
                "op": self._menu_page.checking_cards_op,
                "X-FLOW-ID": self._flow_id,
                "X-CLIENT-ID": self._client_id,
                "X-Requested-With": "XMLHttpRequest",
            },
        )
        card_details = pages.CardDetails(response.text)

        response = self._session.post(
            ROUTER_URL,
            headers={"op": card_details.invoice_op},
            data={"secao": "Cartoes", "item": "Home"},
        )
        cards = response.json()["object"]["data"]

        self._session.post(
            ROUTER_URL,
            headers={"op": card_details.invoice_op},
            data={"secao": "Cartoes:MinhaFatura", "item": ""},
        )

        if not card_name:
            card_id = cards[0]["id"]
        else:
            card_id = next(c for c in cards if c["nome"] == card_name)["id"]

        response = self._session.post(
            ROUTER_URL, headers={"op": card_details.full_statement_op}, data=card_id
        )
        return response.json()

    def get_statements(self, days=90):
        """
        Get and return the statements of the last days.
        """
        response = self._session.post(
            ROUTER_URL,
            data={"periodoConsulta": days},
            headers={
                "op": self._checking_full_statement_page.filter_statements_by_period_op
            },
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
            data={"mesCompleto": "%02d/%d" % (month, year)},
            headers={
                "op": self._checking_full_statement_page.filter_statements_by_month_op
            },
        )
        return response.json()

    def _authenticate2(self):
        response = self._session.post(
            ROUTER_URL,
            data={
                "portal": "005",
                "pre-login": "pre-login",
                "tipoLogon": "7",
                "usuario.agencia": self.agency,
                "usuario.conta": self.account,
                "usuario.dac": self.account_digit,
                "destino": "",
            },
        )
        page = pages.FirstRouter(response.text)
        self._session.cookies.set("X-AUTH-TOKEN", page.auth_token)
        self._op2 = page.secapdk
        self._op3 = page.secbcatch
        self._op4 = page.perform_request
        self._flow_id = page.flow_id
        self._client_id = page.client_id

    def _authenticate3(self):
        self._session.post(
            ROUTER_URL,
            headers={
                "op": self._op2,
                "X-FLOW-ID": self._flow_id,
                "X-CLIENT-ID": self._client_id,
                "renderType": "parcialPage",
                "X-Requested-With": "XMLHttpRequest",
            },
        )

    def _authenticate4(self):
        self._session.post(ROUTER_URL, headers={"op": self._op3})

    def _authenticate5(self):
        response = self._session.post(ROUTER_URL, headers={"op": self._op4})
        page = pages.SecondRouter(response.text)
        self._op5 = page.op_sign_command
        self._op6 = page.op_maquina_pirata
        self._op7 = page.guardiao_cb

    def _authenticate6(self):
        self._session.post(ROUTER_URL, headers={"op": self._op5})

    def _authenticate7(self):
        self._session.post(ROUTER_URL, headers={"op": self._op6})

    def _authenticate8(self):
        response = self._session.post(ROUTER_URL, headers={"op": self._op7})
        page = pages.ThirdRouter(response.text)

        if self.holder_name and page.has_account_holders_form:
            holder, holder_index = page.find_account_holder(self.holder_name)
            self._session.post(
                ROUTER_URL,
                headers={"op": page.op},
                data={
                    "nomeTitular": holder,
                    "indexTitular": holder_index,
                },
            )
            self._authenticate6()
            self._authenticate7()
            response = self._session.post(ROUTER_URL, headers={"op": self._op7})

        page = pages.Password(response.text)
        self._letter_password = page.letter_password(self.password)
        self._op8 = page.op

    def _authenticate9(self):
        response = self._session.post(
            ROUTER_URL,
            headers={"op": self._op8},
            data={"op": self._op8, "senha": self._letter_password},
        )
        self._home = pages.AuthenticatedHome(response.text)

    @cached_property
    def _menu_page(self):
        self._session.post(
            ROUTER_URL, headers={"op": self._home.op, "segmento": "VAREJO"}
        )
        response = self._session.post(ROUTER_URL, headers={"op": self._home.menu_op})
        return pages.Menu(response.text)

    @cached_property
    def _checking_menu_page(self):
        response = self._session.post(
            ROUTER_URL, headers={"op": self._menu_page.checking_account_op}
        )
        return pages.CheckingAccountMenu(response.text)

    @cached_property
    def _checking_statements_page(self):
        response = self._session.post(
            ROUTER_URL, headers={"op": self._checking_menu_page.statements_op}
        )
        return pages.CheckingAccountStatements(response.text)

    @cached_property
    def _checking_full_statement_page(self):
        response = self._session.post(
            ROUTER_URL,
            headers={"op": self._checking_statements_page.full_statement_op},
        )
        return pages.CheckingAccountFullStatement(response.text)
