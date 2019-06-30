pyitau
============

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
