Itaú
============

Unofficial client to access your bank data


How to Use
~~~~~~~~~~~~~
.. code-block:: python

    from itau import Itau

    # Login
    itau = Itau(agency='0000', account='12345', account_digit='5', password='012345')
    itau.authenticate()

    itau.get_statements()


Contributing
~~~~~~~~~~~~~
Contributions are welcome, feel free to open an Issue or Pull Request
