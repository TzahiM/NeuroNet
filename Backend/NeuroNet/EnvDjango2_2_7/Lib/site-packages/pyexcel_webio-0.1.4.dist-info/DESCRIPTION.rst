================================================================================
pyexcel-webio - Let you focus on data, instead of file formats
================================================================================

.. image:: https://raw.githubusercontent.com/pyexcel/pyexcel.github.io/master/images/patreon.png
   :target: https://www.patreon.com/pyexcel

.. image:: https://api.travis-ci.org/pyexcel/pyexcel-webio.svg?branch=master
   :target: http://travis-ci.org/pyexcel/pyexcel-webio

.. image:: https://codecov.io/gh/pyexcel/pyexcel-webio/branch/master/graph/badge.svg
   :target: https://codecov.io/gh/pyexcel/pyexcel-webio

.. image:: https://img.shields.io/gitter/room/gitterHQ/gitter.svg
   :target: https://gitter.im/pyexcel/Lobby


Support the project
================================================================================

If your company has embedded pyexcel and its components into a revenue generating
product, please `support me on patreon <https://www.patreon.com/bePatron?u=5537627>`_ to
maintain the project and develop it further.

If you are an individual, you are welcome to support me too on patreon and for however long
you feel like. As a patreon, you will receive
`early access to pyexcel related contents <https://www.patreon.com/pyexcel/posts>`_.

With your financial support, I will be able to invest
a little bit more time in coding, documentation and writing interesting posts.


Known constraints
==================

Fonts, colors and charts are not supported.

Introduction
================================================================================
**pyexcel-webio** is a tiny interface library to unify the web extensions that uses `pyexcel <https://github.com/pyexcel/pyexcel>`__ . You may use it to write a web extension for your faviourite Python web framework.



Installation
================================================================================

You can install pyexcel-webio via pip:

.. code-block:: bash

    $ pip install pyexcel-webio


or clone it and install it:

.. code-block:: bash

    $ git clone https://github.com/pyexcel/pyexcel-webio.git
    $ cd pyexcel-webio
    $ python setup.py install


Known extensions
=======================

============== ============================
framework      plugin/middleware/extension
============== ============================
Flask          `Flask-Excel`_
Django         `django-excel`_
Pyramid        `pyramid-excel`_
============== ============================

.. _Flask-Excel: https://github.com/pyexcel/Flask-Excel
.. _django-excel: https://github.com/pyexcel/django-excel
.. _pyramid-excel: https://github.com/pyexcel/pyramid-excel


Usage
=========

This small section outlines the steps to adapt **pyexcel-webio** for your favourite web framework. For illustration purpose, I took **Flask** micro-framework as an example.

1. Inherit **ExcelInput** class and implement **load_single_sheet** and **load_book** methods depending on the parameters you will have. For example, **Flask.Request** put the incoming file in **Flask.Request.files** and the key is the field name in the html form::

    from flask import Flask, Request
    import pyexcel as pe
    from pyexcel.ext import webio

    class ExcelRequest(webio.ExcelInput, Request):
        def _get_file_tuple(self, field_name):
            filehandle = self.files[field_name]
            filename = filehandle.filename
            extension = filename.split(".")[1]
            return extension, filehandle

        def load_single_sheet(self, field_name=None, sheet_name=None,
                              **keywords):
            file_type, file_handle = self._get_file_tuple(field_name)
            return pe.get_sheet(file_type=file_type,
                                content=file_handle.read(),
                                sheet_name=sheet_name,
                                **keywords)

        def load_book(self, field_name=None, **keywords):
            file_type, file_handle = self._get_file_tuple(field_name)
            return pe.get_book(file_type=file_type,
                               content=file_handle.read(),
                               **keywords)

2. Plugin in a response method that has the following signature::

       def your_func(content, content_type=None, status=200):
           ....

   or a response class has the same signature::

       class YourClass:
           def __init__(self, content, content_type=None, status=200):
           ....

   For example, with **Flask**, it is just a few lines::

       from flask import Response


       webio.ExcelResponse = Response


3. Then make the proxy for **make_response** series by simply copying the following lines to your extension::

    from pyexcel.ext.webio import (
        make_response,
        make_response_from_array,
        make_response_from_dict,
        make_response_from_records,
        make_response_from_book_dict
    )

Development guide
================================================================================

Development steps for code changes

#. git clone https://github.com/pyexcel/pyexcel-webio.git
#. cd pyexcel-webio

Upgrade your setup tools and pip. They are needed for development and testing only:

#. pip install --upgrade setuptools pip

Then install relevant development requirements:

#. pip install -r rnd_requirements.txt # if such a file exists
#. pip install -r requirements.txt
#. pip install -r tests/requirements.txt

Once you have finished your changes, please provide test case(s), relevant documentation
and update CHANGELOG.rst.

.. note::

    As to rnd_requirements.txt, usually, it is created when a dependent
    library is not released. Once the dependecy is installed
    (will be released), the future
    version of the dependency in the requirements.txt will be valid.


How to test your contribution
------------------------------

Although `nose` and `doctest` are both used in code testing, it is adviable that unit tests are put in tests. `doctest` is incorporated only to make sure the code examples in documentation remain valid across different development releases.

On Linux/Unix systems, please launch your tests like this::

    $ make

On Windows systems, please issue this command::

    > test.bat

How to update test environment and update documentation
---------------------------------------------------------

Additional steps are required:

#. pip install moban
#. git clone https://github.com/moremoban/setupmobans.git # generic setup
#. git clone https://github.com/pyexcel/pyexcel-commons.git commons
#. make your changes in `.moban.d` directory, then issue command `moban`

What is pyexcel-commons
---------------------------------

Many information that are shared across pyexcel projects, such as: this developer guide, license info, etc. are stored in `pyexcel-commons` project.

What is .moban.d
---------------------------------

`.moban.d` stores the specific meta data for the library.

Acceptance criteria
-------------------

#. Has Test cases written
#. Has all code lines tested
#. Passes all Travis CI builds
#. Has fair amount of documentation if your change is complex
#. Please update CHANGELOG.rst
#. Please add yourself to CONTRIBUTORS.rst
#. Agree on NEW BSD License for your contribution



License
================================================================================

New BSD License

Change log
================================================================================

0.1.4 - 23.10.2017
--------------------------------------------------------------------------------

#. `#105 <https://github.com/pyexcel/pyexcel/issues/105>`_, remove gease
   from setup_requires, introduced by 0.1.3.
#. removed testing against python 2.6

0.1.3 - 20.10.2017
--------------------------------------------------------------------------------

added
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

#. `#103 <https://github.com/pyexcel/pyexcel/pull/103>`_, include LICENSE file
   in MANIFEST.in, meaning LICENSE file will appear in the released tar ball.

updated
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

#. Take pyexcel 0.5.5 as dependency


0.1.2 - 12.07.2017
--------------------------------------------------------------------------------

Added
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

#. To bring isave_as and isave_book_as to web clients

Updated
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

#. replaced monkey-patching initialization step. For all extension developer,
   please call init_webio(your_response_function)

0.1.1 - 07.07.2017
--------------------------------------------------------------------------------

Updated
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

#. `#5 <https://github.com/pyexcel/pyexcel-webio/issues/5>`_: explicitly seek
   at 0 for incoming file


0.1.0 - 06.07.2017
--------------------------------------------------------------------------------

Added
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

#. To bring iget_array, iget_records to web clients
#. To facilitate the use of pyexcel-handsontable, pyexcel-pygal,
   pyexcel-matplotlib

0.0.11 - 04.03.2017
--------------------------------------------------------------------------------

Updated
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

#. `#4 <https://github.com/pyexcel/pyexcel-webio/issues/4>`_: extra keywords
   were not passed on to pyexcel

0.0.10 - 22.12.2016
--------------------------------------------------------------------------------

Updated
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

#. `#3 <https://github.com/pyexcel/pyexcel-webio/issues/3>`_: raise exception
   if uploaded file has no content read.


0.0.9 - 22.12.2016
--------------------------------------------------------------------------------

Updated
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

#. Flask-Excel `issue 19 <https://github.com/pyexcel/Flask-Excel/issues/19>`_:
   sheet_name parameter to control sheet name
#. use pyexcel v0.4.0

0.0.8 - 28.10.2016
--------------------------------------------------------------------------------

Updated
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

#. use pyexcel v0.3.0

0.0.7 - 01.06.2016
--------------------------------------------------------------------------------

Updated
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

#. use pyexcel v0.2.2



