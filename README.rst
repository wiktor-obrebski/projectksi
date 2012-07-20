projectksi README
==================

Getting Started
---------------

I assume that you have *virtualenv* and *easy_install* installed in you Python.


First you need use virtualenv package to create a virtual environment.
To do so, invoke the following::

    $ virtualenv --no-site-packages {targetDirectoryName}
    cd {targetDirectoryName}

Parameter *--no-site-packages* is deprecated and used as default in new version of *virtualenv*.
Next you should clone project to this directory and run default setup.py file::

        git clone https://github.com/psychowico/projectksi.git
        cd projectksi
        ../bin/python setup.py develop

Project is ready to go. When you want run it in development mode try::

    ../bin/pserve development.ini

and check *localhost:6543* address.