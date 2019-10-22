Pyitau
======
Unofficial client to access your Itaú bank data

Getting Started
---------------

Prerequisites
`````````````

.. code-block:: python

    pip install pyitau

Installation
````````````

.. code-block:: python

    pip install pyitau

How to use
``````````

.. code-block:: python

    from pyitau import Itau

    # Login
    itau = Itau(agency='0000', account='12345', account_digit='5', password='012345')
    itau.authenticate()

    itau.get_statements()

Contributing
````````````
Contributions are welcome, feel free to open an Issue or Pull Request



