Packaging Janken
================

Janken itself is designed as a
`Python package <https://docs.python.org/3/tutorial/modules.html#packages>`_.
Its hierarchy is simple::

   janken/
       __init__.py
       __main__.py
       data/
           janken_take_10.h5

The :file:`janken_take_10.h5` file is saved, trained Janken model that powers
inference for the Janken package itself. The :file:`__init__.py` module
defines a simple function for inferring the classes of a sequence of input
images, and the :file:`__main__.py` module defines a command-line interface,
so that Janken can be run as an executable.

Preparing Janken for distribution and portable installation involves two
steps:

1. Creating a ``janken`` package definition using
   `Setuptools <https://setuptools.readthedocs.io/en/latest/>`_.
2. Freezing the ``janken`` package into a stand-alone executable using
   `PyInstaller <https://www.pyinstaller.org/index.html>`_.

Janken and Setuptools
---------------------

Setuptools is a collection of enhancements to Python's intrinsic
`distutils <https://docs.python.org/3/library/distutils.html>`_ package
to allow developers to easily build and distribute Python packages,
with features including:

* support for declaring project dependencies
* the ability to declare project "entry points", which supports automatic
  script creation
* the ability to specify data files to be included in packages

The :file:`setup.py` file
+++++++++++++++++++++++++

The build script for ``setuptools`` is a :file:`setup.py` file. It tells
setuptools about the package as well as which code files to include. The
Janken :file:`setup.py` file looks like this:

.. literalinclude:: ../setup.py
   :language: python

Things to highlight here:

1. ``install_requires`` -- Janken requires several other distributions be
   installed when it is in order to run. TensorFlow, for example, is
   required to load the trained model and use it for inference. Pandas is
   used to organize the result of model inference before report to users.
   This keyword argument codifies that requirements list.
2. ``entry_points`` -- Janken, with its :file:`__main__.py` file, is
   configured as an *executable package*, meaning a user with the ``janken``
   package installed could run it like this: ``python -m janken [args]``.
   More convenient for users, however, would be to have a ``janken.exe``
   on the system that they could run directly. The ``entry_points``
   keyword argument defines that executable, asking ``setuptools`` to
   automatically generate scripts and executables for users that install
   the package.
3. ``include_package_data`` -- Janken is only useful if its trained
   model is included in the package. With ``setuptools``, there are
   several options for specifying package data. One is to use the
   ``include_package_data`` keyword, paired with an associated
   :file:`MANIFEST.in` file that specifies the specific data files to
   include. The Janken manifest contains a single entry, for the
   :file:`janken_take_10.h5` model file.

Creation and installation of distribution packages
++++++++++++++++++++++++++++++++++++++++++++++++++

Generating
`distribution packages <https://packaging.python.org/glossary/#term-Distribution-Package>`_
for Janken is simple. The most common distribution formats are
*source distributions*, packaged as ``.tar.gz`` source archives, and
*built distributions*, packaged as ``.whl`` files, or "wheels". The
:file:`setup.py` script supports commands to generate either:

.. note::

   Running :file:`setup.py`, and in particular to generate wheel files,
   requires that you have ``setuptools`` and ``wheel`` installed in your
   Python environment!

.. code-block:: console

   # Generate a source distribution for Janken
   python setup.py sdist

   # Generate a wheel for Janken
   python setup.py bdist_wheel

Running these commands should generate two files in the local ``dist/``
directory::

   dist/
       janken-0.0.1-py3-none-any.whl
       janken-0.0.1.tar.gz

The :file:`setup.py` script can also be used to install the ``janken``
package into the current active Python environment, either directly:

.. code-block:: console

   python setup.py install

Or via :program:`pip`, pointing :program:`pip` to the directory where the
:file:`setup.py` file can be found:

.. code-block:: console

   pip install .

.. warning::

   Though the two approaches for installations are generally equivalent,
   direct invocation of :file:`setup.py` and invocation through
   :program:`pip` use different means of dependency resolution, which can
   result in different behavior. Because :file:`setup.py` can do the
   wrong things for many dependencies, it is highly recommended to use
   :program:`pip`! See the answer to this Stack Overflow
   `question <https://stackoverflow.com/questions/19048732/python-setup-py-develop-vs-install>`_
   to learn more.

There are developer versions of those install commands as well, which
installs the package in "development mode", making Janken available
in the active Python environment, but referring to the project's current
source code, so that any changes to Janken code are immediately seen by
the environment. Those analogous commands are:

.. code-block:: console

   # The setup.py method
   python setup.py develop

   # The pip method
   pip install -e .

Freezing Janken with PyInstaller
--------------------------------

Source and built distributions are convenient and popular ways to make
Python packages like Janken available to users. In both cases, however,
users are expected to have a Python interpreter installed on their system,
with Janken's package dependencies (like TensorFlow and Pandas) either
already installed, or avaiable to install. For prospective users
unfamiliar with Python or package managers like :program:`pip` and
Anaconda's :program:`conda`, those distributions look considerably less
convenient.

Enter *PyInstaller*. PyInstaller bundles a Python application and all
its dependencies into a single package. Users can run the packaged
application without installing an interpreter or any modules. It supports
bundling to a single folder or even a single file. Distribution becomes
as simple as zipping the folder or file up as ``janken.zip`` and
transmitting it to users.

For typical Python scripts, using PyInstaller is a two step process:

1. Run ``pyinstaller myscript.py`` to generate a :file:`myscript.spec` file.
2. Run ``pyinstaller myscript.spec`` to generate a PyInstaller bundle
   for :file:`myscript.py`.

The Janken ``.spec`` file
+++++++++++++++++++++++++

The spec file tells PyInstaller how to process the script when bundling,
and can be modified as needed, for example to specify data files that
should be included in the bundle.

Janken isn't quite a typical Python script--instead, it is designed
so that its executable script, :program:`janken`, is automatically
generated by ``setuptools`` as an "entry point". PyInstaller does not
know how to interpret scripts which load entry points, and therefore
cannot generate valid ``.spec`` files where entry points are concerned.

Fortunately, PyInstaller's Wiki includes a
`recipe for packaging from a Setuptools entry point
<https://github.com/pyinstaller/pyinstaller/wiki/Recipe-Setuptools-Entry-Point>`_.
Janken is bundled using a ``.spec`` file based on that recipe; it looks like
this:

.. literalinclude:: ../janken_pyinstaller.spec
   :language: python

Essentially, it creates an *entry point definition* which automatically
creates a script equivalent to the entry point, but in a format that
PyInstaller can analyze. It does that analysis and uses the results to
define an otherwise standard package ``.spec``.

Things to highlight here:

1. ``datas`` -- The ``Entrypoint`` function is called with a ``datas``
   keyword argument to help PyInstaller understand what data files
   should be included in the bundle. Since all Janken data files
   are in package directory ``janken/data``, the ``datas`` argument
   is defined accordingly.
2. ``hiddenimports`` -- Sometimes, packages import things in a way that
   is not visible or discoverable by PyInstaller. This is true with
   Janken, whose use of Pandas' :func:`to_markdown` function requires
   an optional Pandas dependency, ``tabulate``, be installed. PyInstaller
   is made aware of that hidden import via the ``hiddenimports`` keyword
   argument.

Bundling Janken
+++++++++++++++

Bundling Janken using its :file:`janken_pyinstaller.spec` file is
straightforward:

.. code-block:: console

   # Generate a single folder PyInstaller bundle for Janken
   pyinstaller janken_pyinstaller.spec

The above command will create a ``dist/janken/`` folder which
can then be compressed for distribution to users. For example, in
PowerShell:

.. code-block:: powershell

   Compress-Archive -Path .\dist\janken Janken.zip
