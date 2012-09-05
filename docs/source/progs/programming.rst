===========
Programming
===========

.. note::
    This file will be extend by psychowico in short time.

Used technologies
=================

To now we use in code following technologies:

* Pyramid_
* jinja2_
* jQuery_
* `Twitter Bootstrap`_
* LESS_
* squeezeit_
* pyramid_viewscomposer_
* pyramid_debugtoolbar_
* sqlalchemy_

Pyramid
-------

.. note::
    Pyramid is a small, fast, down-to-earth Python web application development framework.

We use Pyramid framework to build our application. `Check it documentation`_, most important is to
understand how *view_config*  decorator work. We starting our work with version 1.3.

.. _`Check it documentation`: http://docs.pylonsproject.org/en/latest/docs/pyramid.html

jinja2
------

.. note::
    Jinja2 is a modern and designer friendly templating language for Python.

As our template language we choose Jinja2. Understanding it should be easy, it's a quite intuitive.
You found can `documentation here`_.

.. _`documentation here`: http://jinja.pocoo.org/docs/

jQuery
------

.. note::
    jQuery is designed to change the way that you write JavaScript.

And it did this. Today jQuery is a standard library used in thousand of projects, it's make JavaScript programming
easy and more fun. If you don't know it, you should read something there_.

.. _there: http://jquery.com/

Twitter Bootstrap
-----------------

.. note::
    Simple and flexible HTML, CSS, and Javascript for popular user interface components and interactions.

It give our standard pack of css classes, jQuery plugins and html things. It make much easier making nice looking
interface. You can found `more info there`_.

.. _`more info there`: http://twitter.github.com/bootstrap/

LESS
----

.. note::
    The *dynamic* stylesheet language.

Like in description - this give us language that can generate css in nice way, instead of writing it all static.
It give our many benefits, their documentation_ describe this nice.
You can check *static/css/projectksi.less* file, there is all our LESS code for now.

.. _documentation: http://lesscss.org/

squeezeit
---------

.. note::
    Squeezeit - Python CSS and Javascript minifier Copyright (C) 2011 Sam Rudge

**squeezeit** is a Python library writed by *Sam Rudge*. It help us managing js, css and less libraries.
It was written at python2, but I made a bridge to python3 version, `fallow this link`_ to read more.
It minifying, combining and gzip'ing bundles of Javascript and CSS files. It is critical for lower
our site needed requests and download less data - and have happy users. There you can read more about
:ref:`our squeezeit implementation <web-deps>`.

.. _`fallow this link`: https://github.com/psychowico/Squeezeit


pyramid_viewscomposer
---------------------

.. note::
    Pyramid add-on that adding to framework new decorator composer_view_config, working analogously to build-in view_config decorator.

It our own writed plugin for pyramid, you can found some info at it `github site`_.

.. _`github site`: https://github.com/psychowico/pyramid_viewscomposer

pyramid_debugtoolbar
--------------------

.. note::
    *pyramid_debugtoolbar* provides a debug toolbar useful while you’re developing a Pyramid application.

We use it only in developing time. It is standard for pyramid developing, you can read about it functionality
 in `pyramid framework docs`_.

 .. _`pyramid framework docs`: http://docs.pylonsproject.org/projects/pyramid_debugtoolbar/en/latest/

sqlalchemy
--------------------

.. note::
    SQLAlchemy is the Python SQL toolkit and Object Relational Mapper that gives application developers the full power and flexibility of SQL.

Most popular ORM for python developers. We use it in rather default way. Engine object is created from config file,
in our program *main* method, session are prepared in *projectksi.models.tables* submodule.

.. code-block:: python

    DBSession = scoped_session(sessionmaker(extension=ZopeTransactionExtension()))

We use *ZopeTransactionExtension* for support to automatic transaction system. With this extension we do not need
commit our transactions after proper request, and aborts them in error case - this will be provided by system.
*scoped_session* making working with session in our application easier - you can read more about this
at `sqlalchemy docs site`_.

By default we use oursql_ driver for sqlalchemy, in version p3k (with python 3 support). To change this look
to you config file:

    *sqlalchemy.url = mysql+oursql://root:root@localhost:3306/ksi.test*

.. _`sqlalchemy docs site`: http://docs.sqlalchemy.org/en/rel_0_7/orm/session.html#sqlalchemy.orm.scoping.ScopedSession
.. _oursql: http://packages.python.org/oursql/


Plugins system
==============

Our application was logically divided to plugins. As plugin we mean python package that is directly
related only to projectksi.* package - no directly related with another plugins. So, this packages
can not *import* each other. Main goal of this was create packages that can be easly removed and added
back to game - to enable/disable specific game features. For situation in which lack of plugins relationship
will result repetition code we create class that implement *ServiceLocator* pattern. This gives us
confidence that:

* Components do not know each other directly
* Components specify external dependencies using some sort of a key
* Dependencies are resolved late, preferably just before they are used (JIT dependency resolution)
* Dependencies are resolved once for each component

Below you can found usage cases to understand this issue better.

Create plugin
-------------

To create new plugin you need prepare python empty package and prepare class inherited from
*projectksi.core.plugins.PluginAbstract*. Next you should implement some base interface for it, in
your main *__init__.py* file.

.. code-block:: python

    from projectksi.core import plugins

    class MyPlugin(plugins.PluginAbstract):

        def unique_name(self):
            return "my_plugin_$#@%#@(%"

        def readable_name(self):
            return "Testing plugin"

        def description(self):
            return 'My plugin created for tests'

        def depending(self):
            """ tuple of unique_name without which this particular plugin
             can not working
            """
            return ()

        def services_depending(self):
            """ tuple of service (from ServiceLocator) keys without which this particular plugin
            can not working. This will be visible for debug purposes.
            """
            return ()


        def includeme(self, config, service_locator):
            #if you want use @view_config or @compose_view_config decorators in you plugin you need
            #add this line
            config.scan()

This plugin doing nothing of course. To make it accessible in game your need move your package to
*plugins* directory in game main folder. Next you need open you config file and add your package
name to *projectksi.plugins* section. For sample if your package is named "*my_new_plugin*":


    |    *projectksi.plugins =*
    |        *plugins.test_plugin*
    |        *plugins.my_new_plugin*

Plugins naming
--------------

You need provide some info about your plugin. You must do it by *unique_name*, *readable_name*
and *description* methods. *readable_name* and *description* are used for later debuging, it
is a quite important to give plugin name and description to others developers, and you for few
month, can easily guess what exactly this plugin do for game. *unique_name* will be used by plugin
system and should be (surprise) unique.

Plugins dependencies
--------------------

You need specify plugin dependencies - from others plugins and for services. Now both can be used
for debug purposes, but probably system will be inspect this data later.

First you need specify dependencies from another plugins:

.. code-block:: python

    class MyPlugin(plugins.PluginAbstract):
        ...

        def depending(self):
            """ tuple of unique_name without which this particular plugin
            can not working
            """
            return ("testing_plugin_#@%#@%")

It should be tuple of plugins unique names. Dependencies will probably mean that your plugin use
services provided by anothers plugins.

Next you should describe services that your plugin will use.

.. code-block:: python

    class MyPlugin(plugins.PluginAbstract):
        ...

        def services_depending(self):
            """ tuple of service (from ServiceLocator) keys without which this particular plugin
            can not working. This will be visible for debug purposes.
            """
            return ("auth-service", "item-generator", "random-number-generator")

You can read more about services below.

Plugin services(ServiceLocator)
-------------------------------

Plugin can provide services, or use services provided by anothers plugins. It is make by ServiceLocator
object, that you getting in "includeme" method. ServiceLocator object provide for you four methods:

.. code-block:: python

    class ServiceLocator(object):

        def has(self, key_or_alias):
            ...

        def get(self, key_or_alias):
            ...

        def set(self, key, service, can_override = False):
            ...

        def create_alias(self, alias, key_or_alias):
            ...

It is a quite simple class. It give your possibility to register services (*set*), checking
service existence(*has*), fetching services(*get*) or create aliases - it is mean a simple
shortcut for existing service. Below you can see example of providing simple service by
plugin:

.. code-block:: python

    class MyPlugin(plugins.PluginAbstract):
        ...

        def url_service(self):
            def popular_url(name):
                if name=="docs":
                    return "http://docs.projectksi.com/"
                elif name=="site":
                    return "http://projectksi.com/"
                elif name=="secret":
                    return "http://my-secret-url.com/"
            return popular_url

        def includeme(self, config, service_locator):
            service_locator.set('url-service', self.url_service)

            #if you want use @view_config or @compose_view_config decorators in you plugin you need
            #add this line
            config.scan()


So, what this code do? It register in service_locator 'url-service' service. When first client (probably
another plugin) will call it, by:

.. code-block:: python

        popular_url_service = service_locator.get('url-service')
        print(popular_url_service("docs"))
        print(popular_url_service("site"))
        print(popular_url_service("secret"))

*url_service(self)* method will be called. It result (*popular_url()* method) will be stored in ServiceLocator
cache. When next plugins will call it, result of first call will be used. In this case it can look a quite
little need, but often we will return a object of some class - and we want postpone creation of it so long
as this will be needed. For sample, our method can call database instead of return static string. It is
obvious that we want call database if it is not really necessary.

Plugins and Pyramid framework
-----------------------------

In plugin class *includeme* method you will receive a instance of *config* object. You can use it like with
standard Pyramid extensions. For sample, you can register you own route and view:

.. code-block:: python

    def includeme(self, config, service_locator):
        ...

        config.add_route('my-plugin-route', '/my-plugin-route')
        config.add_view(self.MyViewMethod, route_name='my-plugin-route')

        ...

        config.scan()

If you want use declarative views registration you need remember about calling *config.scan()* method
at end of *includeme* function.

Debugging plugins
-----------------

You can use Pyramid debug panel to get some basic information about current loaded plugins. You should
check "Introspection" section and "Projectksi plugins" group.

How to
======

Fetching data from database in your views
-----------------------------------------

You need simple import *DBSession* object from *projectksi.models.tables* and use it in standard, sqlalchemy, way.
All sqlalchemy models you will find in *projectksi.models* package.

.. code-block:: python

    ...
    from projectksi.models.tables import DBSession

    @view_config(route_name='home', renderer='test.jinja2')
    def my_view(request):
        user = DBSession.query(tables.User).first()
        val = user.email if user else 'empty database'
        return {'email':val}

If you need learn about working with sqlalchemy `try check this tutorial`_.

.. _`try check this tutorial`: http://docs.sqlalchemy.org/en/rel_0_7/orm/tutorial.html