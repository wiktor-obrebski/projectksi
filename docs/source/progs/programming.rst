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
* WebDeps_
* pyramid_viewscomposer_
* pyramid_debugtoolbar_

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
You can check *static/css/projectksi.less* file, there is all our LESS code for now. This file is including to
templates by *WebDeps*.

.. _documentation: http://lesscss.org/

WebDeps
-------

WebDeps is a Python library writed by *Nando Florestan*. It help us managing js, css and less libraries.
On our site you can found :ref:`compiled documentation <web-deps>` for it.


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
