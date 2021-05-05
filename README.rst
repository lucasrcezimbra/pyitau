pyitau
============

.. image:: https://badge.fury.io/py/pyitau.svg
    :target: https://badge.fury.io/py/pyitau
    :alt: PyPI
.. image:: https://travis-ci.org/lucasrcezimbra/pyitau.svg?branch=master
    :target: https://travis-ci.org/lucasrcezimbra/pyitau
    :alt: Travis CI Build
.. image:: https://coveralls.io/repos/github/lucasrcezimbra/pyitau/badge.svg?branch=master
    :target: https://coveralls.io/github/lucasrcezimbra/pyitau?branch=master
    :alt: Coverage
.. image:: https://pyup.io/repos/github/lucasrcezimbra/pyitau/shield.svg
    :target: https://pyup.io/repos/github/lucasrcezimbra/pyitau/
    :alt: Updates
.. image:: https://pyup.io/repos/github/lucasrcezimbra/pyitau/python-3-shield.svg
    :target: https://pyup.io/repos/github/lucasrcezimbra/pyitau/
    :alt: Python 3

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
Contributions are welcome, feel free to open an Issue or Pull Request

~~~~~~~~~~~~~

[ ~ Dependencies scanned by PyUp.io ~ ]
