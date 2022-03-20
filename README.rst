pyitau
============

.. image:: https://badge.fury.io/py/pyitau.svg
    :target: https://badge.fury.io/py/pyitau
    :alt: PyPI
.. image:: https://coveralls.io/repos/github/lucasrcezimbra/pyitau/badge.svg?branch=master
    :target: https://coveralls.io/github/lucasrcezimbra/pyitau?branch=master
    :alt: Coverage
.. image:: https://pyup.io/repos/github/lucasrcezimbra/pyitau/shield.svg
    :target: https://pyup.io/repos/github/lucasrcezimbra/pyitau/
    :alt: Updates

Unofficial client to access your Itaú bank data


Installation
~~~~~~~~~~~~~
``pip install pyitau``


How to Use
~~~~~~~~~~~~~
.. code-block:: python

    from pyitau import Itau

    # Login
    itau = Itau(agency='0000', account='12345', account_digit='5', password='012345')
    itau.authenticate()

    itau.get_statements()


Contributing
~~~~~~~~~~~~~
Contributions are welcome, feel free to open an Issue or Pull Request.

Pull requests must be for the `develop` branch.

.. code-block:: bash

    git clone https://github.com/lucasrcezimbra/pyitau
    cd pyitau
    git checkout develop
    python -m venv .venv
    pip install -r requirements-dev.txt
    pre-commit install
    pytest


~~~~~~~~~~~~~

[ ~ Dependencies scanned by PyUp.io ~ ]
