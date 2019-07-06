import re

import requests
from bs4 import BeautifulSoup


ITAU_URL = 'https://www.itau.com.br'
ROUTER_URL = 'https://internetpf2.itau.com.br/router-app/router'


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
        self._authenticate0()
        self._authenticate1()
        self._authenticate2()
        self._authenticate3()
        self._authenticate4()
        self._authenticate5()
        self._authenticate6()
        self._authenticate7()
        self._authenticate8()
        self._authenticate9()

    def get_statements(self):
        op = self._home.find('div', class_='logo left').find('a').attrs['data-op']

        headers = {'op': op, 'segmento': 'VAREJO'}
        response = self._session.post(ROUTER_URL, headers=headers)
        op2 = re.search(
            'urlBox : "(.*?)".*seletorContainer : "#boxContaCorrente",',
            response.text,
            flags=re.DOTALL,
        ).group(1)

        response = self._session.post(ROUTER_URL, headers={'op': op2})
        op3 = re.search(
            'urlBox : "(.*?)".*seletorContainer : ".conteudoBoxContaCorrente",',
            response.text,
            flags=re.DOTALL,
        ).group(1)

        response = self._session.post(ROUTER_URL, headers={'op': op3})
        soup = BeautifulSoup(response.text, features='html.parser')
        op4 = soup.find('a').attrs['data-op']

        response = self._session.post(ROUTER_URL, headers={'op': op4})
        pattern = 'function consultarLancamentosPorPeriodo.*' \
                  '"periodoConsulta" : parametrosPeriodo.*' \
                  'url = "(.*?)";'
        op5 = re.search(
            pattern,
            response.text,
            flags=re.DOTALL,
        ).group(1)

        response = self._session.post(
            ROUTER_URL, data={'periodoConsulta': 90}, headers={'op': op5})
        return response.json()

    def _authenticate0(self):
        response = self._session.get(ITAU_URL)
        soup = BeautifulSoup(response.text, features='html.parser')
        form = soup.find('form', attrs={'name': 'banklineAgConta'})
        self._id = form.find('input', attrs={'name': 'id'}).attrs['value']
        self._op1 = form.find('input', attrs={'name': 'op'}).attrs['value']

    def _authenticate1(self):
        data = {
            'id': self._id,
            'op': self._op1,
            'agencia': self.agency,
            'conta': self.account,
            'dac': self.account_digit,
            'tipousuario': 'X',
            'origem': 'H'
        }
        url = 'https://bankline.itau.com.br/GRIPNET/bklcom.dll'
        self._session.post(url, data=data)

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

        auth_token = re.search("authToken=\\'(.*?)\\';", response.text).group(1)
        self._session.cookies.set('X-AUTH-TOKEN', auth_token)

        self._op2 = re.search("\$SECAPDK.uidap\(\'(.*?)\'\);", response.text).group(1)
        self._op3 = re.search("\$SECBCATCH.uidap\(\'(.*)\'\);", response.text).group(1)
        self._op4 = re.search('router.performRequest\("(.*?)", ', response.text).group(1)
        self._flow_id = re.search("var flowId=\'(.*)\';", response.text).group(1)
        self._client_id = re.search("var clientId=\'(.*?)\';", response.text).group(1)

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
        self._op5 = re.search('__opSignCommand = "(.*?)";', response.text).group(1)
        self._op6 = re.search('__opMaquinaPirata = "(.*?)";', response.text).group(1)
        self._op7 = re.search(
            'var guardiao_cb = function\(\) {\n\t\t\tloadPage\(\'(.*?)\'\);',
            response.text
        ).group(1)

    def _authenticate6(self):
        headers = {'op': self._op5}
        self._session.post(ROUTER_URL, headers=headers)

    def _authenticate7(self):
        headers = {'op': self._op6}
        self._session.post(ROUTER_URL, headers=headers)

    def _authenticate8(self):
        headers = {'op': self._op7}
        response = self._session.post(ROUTER_URL, headers=headers)

        soup = BeautifulSoup(response.text, features='html.parser')

        self._op8 = soup.find('input', id='op').attrs['value']

        keys = soup.find(class_='teclado') \
                   .find(class_='teclas') \
                   .findAll(class_='campoTeclado')
        password_mapper = {}
        for key in keys:
            numbers = key.attrs['aria-label'].split(' ou ')
            letter = key.attrs['rel'][0].replace('tecla_', '')
            password_mapper[numbers[0]] = letter
            password_mapper[numbers[1]] = letter

        self._letter_password = ''
        for char in self.password:
            self._letter_password += password_mapper[char]

    def _authenticate9(self):
        headers = {'op': self._op8}
        data = {
            'op': self._op8,
            'senha': self._letter_password
        }

        response = self._session.post(ROUTER_URL, headers=headers, data=data)
        self._home = BeautifulSoup(response.text, features='html.parser')
