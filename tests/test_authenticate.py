import responses

from pyitau.main import ROUTER_URL


@responses.activate
def test_authenticate2(itau, mocker, response_authenticate2):
    responses.add(responses.POST, ROUTER_URL, body=response_authenticate2)
    post_spy = mocker.spy(itau._session, "post")

    itau._authenticate2()

    expected_data = {
        "portal": "005",
        "pre-login": "pre-login",
        "tipoLogon": "7",
        "usuario.agencia": itau.agency,
        "usuario.conta": itau.account,
        "usuario.dac": itau.account_digit,
        "destino": "",
    }
    post_spy.assert_called_once_with(ROUTER_URL, data=expected_data)
    assert itau._session.cookies.get("X-AUTH-TOKEN") == "PYITAU_AUTHTOKEN"
    assert itau._client_id == "PYITAU_CLIENTID"
    assert itau._flow_id == "PYITAU_FLOWID"
    assert itau._op2 == "PYITAU_OP2"
    assert itau._op3 == "PYITAU_OP3"
    assert itau._op3 == "PYITAU_OP3"
    assert itau._op4 == "PYITAU_OP4"


@responses.activate
def test_authenticate3(itau, mocker):
    responses.add(responses.POST, ROUTER_URL)
    post_spy = mocker.spy(itau._session, "post")

    itau._op2 = "PYITAU_OP2"
    itau._client_id = "PYITAU_CLIENTID"
    itau._flow_id = "PYITAU_FLOWID"

    itau._authenticate3()

    expected_headers = {
        "op": itau._op2,
        "X-FLOW-ID": itau._flow_id,
        "X-CLIENT-ID": itau._client_id,
        "renderType": "parcialPage",
        "X-Requested-With": "XMLHttpRequest",
    }
    post_spy.assert_called_once_with(ROUTER_URL, headers=expected_headers)


@responses.activate
def test_authenticate4(itau, mocker):
    responses.add(responses.POST, ROUTER_URL)
    post_spy = mocker.spy(itau._session, "post")

    itau._op3 = "PYITAU_OP3"

    itau._authenticate4()

    expected_headers = {"op": itau._op3}
    post_spy.assert_called_once_with(ROUTER_URL, headers=expected_headers)


@responses.activate
def test_authenticate5(itau, mocker, response_authenticate5):
    responses.add(responses.POST, ROUTER_URL, body=response_authenticate5)
    post_spy = mocker.spy(itau._session, "post")

    itau._op4 = "PYITAU_OP4"

    itau._authenticate5()

    expected_headers = {"op": itau._op4}
    post_spy.assert_called_once_with(ROUTER_URL, headers=expected_headers)
    assert itau._op5 == "PYITAU_OP5"
    assert itau._op6 == "PYITAU_OP6"
    assert itau._op7 == "PYITAU_OP7"


@responses.activate
def test_authenticate6(itau, mocker):
    responses.add(responses.POST, ROUTER_URL)
    post_spy = mocker.spy(itau._session, "post")

    itau._op5 = "PYITAU_OP5"

    itau._authenticate6()

    expected_headers = {"op": itau._op5}
    post_spy.assert_called_once_with(ROUTER_URL, headers=expected_headers)


@responses.activate
def test_authenticate7(itau, mocker):
    responses.add(responses.POST, ROUTER_URL)
    post_spy = mocker.spy(itau._session, "post")

    itau._op6 = "PYITAU_OP6"

    itau._authenticate7()

    expected_headers = {"op": itau._op6}
    post_spy.assert_called_once_with(ROUTER_URL, headers=expected_headers)


@responses.activate
def test_authenticate8(itau, mocker, response_authenticate8):
    responses.add(responses.POST, ROUTER_URL, body=response_authenticate8)
    post_spy = mocker.spy(itau._session, "post")

    itau._op7 = "PYITAU_OP7"

    itau._authenticate8()

    expected_headers = {"op": itau._op7}
    post_spy.assert_called_once_with(ROUTER_URL, headers=expected_headers)
    assert itau._op8 == "PYITAU_OP8"
    assert itau._letter_password is not None


@responses.activate
def test_authenticate9(itau, mocker):
    responses.add(responses.POST, ROUTER_URL)
    post_spy = mocker.spy(itau._session, "post")

    itau._op8 = "PYITAU_OP8"
    itau._letter_password = "ABCDEF"

    itau._authenticate9()

    expected_headers = {"op": itau._op8}
    expected_data = {"op": itau._op8, "senha": itau._letter_password}
    post_spy.assert_called_once_with(
        ROUTER_URL, headers=expected_headers, data=expected_data
    )
    assert itau._home is not None
