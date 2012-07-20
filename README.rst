projectksi README
==================

Getting Started
---------------

First you need virtualenv package. Once the virtualenv package is installed in your Python,
you can then create a virtual environment. To do so, invoke the following:

    $ virtualenv --no-site-packages {targetDirectoryName}

Parameter *--no-site-packages* is deprecated and used as default in new version of *virtualenv*.

    cd {targetDirectoryName}

Next you should clone project to this directory and run default setup.py file::

        git clone https://github.com/psychowico/projectksi.git
        cd projectksi
        ../bin/python setup.py develop

Project is ready to go. When you want run it in development mode try:

    ../bin/pserve development.ini

and check *localhost:6543* address.