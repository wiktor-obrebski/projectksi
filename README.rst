projectksi README
==================

You can read full documentation on http://docs.projectksi.com/.

Getting Started
---------------

I assume that you have *virtualenv* and *easy_install* installed in your Python.


First you need use virtualenv package to create a virtual environment.
To do so, invoke the following::

    $ virtualenv --no-site-packages --python=/usr/bin/python3.2 {targetDirectoryName} 
    cd {targetDirectoryName}

Parameter *--no-site-packages* is deprecated and used as default in new version of *virtualenv*.
Next you should clone project to this directory and run default setup.py file::

        git clone https://github.com/psychowico/projectksi.git
        cd projectksi
        ../bin/python setup.py develop

You need two additional dependencies in system to make our building process working correctly.
It will be compiler for LESS_ files and compiler for COFFEE_ files. First you should install
'node-less' package. It will be needed in 'production' environment. On Ubuntu it should work:

    sudo apt-get install node-less

Next you will need CoffeeScriptRedux_. Download it and follow their github page instructions.
At end you need tell our builder where their *bin/coffee* file is. Easiest way is create a link
to it. If you are in main "CoffeeScriptRedux" directory, you can create it by:

    sudo ln -s ./bin/coffee /usr/bin/coffee-redux-comp

Or by modify *projectksi.web_deps.coffee_compiler.path* project configuration directive.

.. _LESS: http://lesscss.org/
.. _COFFEE: http://coffeescript.org/
.. _CoffeeScriptRedux: https://github.com/michaelficarra/CoffeeScriptRedux/

Project is ready to go. When you want run it in development mode try::

    ../bin/pserve development.ini

and check *localhost:6543* address.
