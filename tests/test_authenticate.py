import responses

from pyitau.main import ITAU_URL


@responses.activate
def test_authenticate0(itau, mocker):
    with open('./tests/responses/itau.html') as file:
        body = file.read()
    responses.add(responses.GET, ITAU_URL, body=body)
    get_spy = mocker.spy(itau._session, 'get')

    itau._authenticate0()

    get_spy.assert_called_once_with(ITAU_URL)
    assert itau._id is not None
    assert itau._op1 is not None


@responses.activate
def test_authenticate1(itau, mocker):
    url = 'https://bankline.itau.com.br/GRIPNET/bklcom.dll'
    responses.add(responses.POST, url)
    post_spy = mocker.spy(itau._session, 'post')
    itau._id = 'ID'
    itau._op1 = 'OP1'

    itau._authenticate1()

    expected_data = {
        'id': itau._id,
        'op': itau._op1,
        'agencia': itau.agency,
        'conta': itau.account,
        'dac': itau.account_digit,
        'tipousuario': 'X',
        'origem': 'H'
    }
    post_spy.assert_called_once_with(url, data=expected_data)
