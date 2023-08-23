Changelog
=========


1.3.0 (2023-08-23)
------------------
* Add support for multiple cards `#205`_ and `#209`_. Thanks to `@ivancrneto`_
* Fix credit card statements `#205`_ and `#209`_. Thanks to `@ivancrneto`_
* Add support for multiple holders `#204`_ and `#207`_. Thanks to `@ivancrneto`_
* Rename pages removing Page
* Fix pre-commit hooks
* Add ruff and black as pre-commit hooks

.. _`@ivancrneto`: https://github.com/ivancrneto
.. _`#204`: https://github.com/lucasrcezimbra/pyitau/pull/204
.. _`#205`: https://github.com/lucasrcezimbra/pyitau/pull/205
.. _`#207`: https://github.com/lucasrcezimbra/pyitau/pull/207
.. _`#209`: https://github.com/lucasrcezimbra/pyitau/pull/209


1.2.2 (2023-03-12)
------------------
* Add support for monthly statements. Thanks to `@davibobsin`_
* Refactor Checking Account statements
* Add cached-property as requirement
* Update dev requirements
* Fix GitHub publish Action

.. _`@davibobsin`: https://github.com/davibobsin


1.1.0 (2022-07-31)
------------------
* Add credit card support `#171`_. Thanks to `@joaoalvarenga`_
* Add ReadTheDocs
* Change from pyup to dependabot
* Update dev requirements

  * pre-commit 2.17.0 ~> 2.20.0
  * pytest 7.1.1 ~> 7.1.2
  * pytest-mock 3.7.0 ~> 3.8.2
  * sphinx 4.4.0 ~> 5.0.2

.. _`#171`: https://github.com/lucasrcezimbra/pyitau/issues/171


1.0.3 (2022-03-19)
------------------
* Fix authentication. Thanks to `@joaoalvarenga`_
* Refactor get_statements `#107`_
* Update dev requirements

.. _`#107`: https://github.com/lucasrcezimbra/pyitau/issues/107
.. _`@joaoalvarenga`: https://github.com/joaoalvarenga


1.0.2 (2021-12-13)
------------------
* Fix authentication error `#151`_
* Update dev requirements
* Fix CI

.. _`#151`: https://github.com/lucasrcezimbra/pyitau/issues/151


1.0.1 (2021-09-04)
------------------
* Fix authentication error 'Connection reset by peer'
* Moves CI from Travis to Github Actions `#141`_
* Add initial structure for Sphinx documentation `#16`_. Thanks to `@DuyguKeskek`_
* Update dev requirements
* Adds pre-commit `#108`_

.. _`#16`: https://github.com/lucasrcezimbra/pyitau/issues/16
.. _`#108`: https://github.com/lucasrcezimbra/pyitau/issues/108
.. _`#141`: https://github.com/lucasrcezimbra/pyitau/issues/141
.. _`@DuyguKeskek`: https://github.com/DuyguKeskek


1.0.0 (2021-05-05)
------------------
* Refactor `#93`_ and first stable version

.. _`#93`: https://github.com/lucasrcezimbra/pyitau/issues/93


0.0.6 (2021-05-04)
------------------
* Fix access to the homepage that was changed `#102`_
* Update requirements-dev

.. _`#102`: https://github.com/lucasrcezimbra/pyitau/issues/102


0.0.5 (2019-07-05)
------------------
* Get statements from last 90 days `#5`_

.. _`#5`: https://github.com/lucasrcezimbra/pyitau/issues/5


0.0.4 (2019-06-30)
------------------
* First pypi version
