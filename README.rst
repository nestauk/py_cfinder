========
Overview
========

.. start-badges

.. list-table::
    :stub-columns: 1

    * - docs
      - |docs|
    * - tests
      - | |travis|
        |
    * - package
      - | |version| |wheel| |supported-versions| |supported-implementations|
        | |commits-since|

.. |docs| image:: https://readthedocs.org/projects/py_cfinder/badge/?style=flat
    :target: https://readthedocs.org/projects/py_cfinder
    :alt: Documentation Status


.. |travis| image:: https://travis-ci.org/georgerichardson/py_cfinder.svg?branch=master
    :alt: Travis-CI Build Status
    :target: https://travis-ci.org/georgerichardson/py_cfinder

.. |version| image:: https://img.shields.io/pypi/v/py-cfinder.svg
    :alt: PyPI Package latest release
    :target: https://pypi.python.org/pypi/py-cfinder

.. |commits-since| image:: https://img.shields.io/github/commits-since/georgerichardson/py_cfinder/v0.1.0.svg
    :alt: Commits since latest release
    :target: https://github.com/georgerichardson/py_cfinder/compare/v0.1.0...master

.. |wheel| image:: https://img.shields.io/pypi/wheel/py-cfinder.svg
    :alt: PyPI Wheel
    :target: https://pypi.python.org/pypi/py-cfinder

.. |supported-versions| image:: https://img.shields.io/pypi/pyversions/py-cfinder.svg
    :alt: Supported versions
    :target: https://pypi.python.org/pypi/py-cfinder

.. |supported-implementations| image:: https://img.shields.io/pypi/implementation/py-cfinder.svg
    :alt: Supported implementations
    :target: https://pypi.python.org/pypi/py-cfinder


.. end-badges

A Python wrapper for the CFinder tool.

* Free software: MIT license

Installation
============

::

    pip install py-cfinder

Documentation
=============


https://py_cfinder.readthedocs.io/


Development
===========

To run the all tests run::

    tox

Note, to combine the coverage data from all the tox environments run:

.. list-table::
    :widths: 10 90
    :stub-columns: 1

    - - Windows
      - ::

            set PYTEST_ADDOPTS=--cov-append
            tox

    - - Other
      - ::

            PYTEST_ADDOPTS=--cov-append tox
