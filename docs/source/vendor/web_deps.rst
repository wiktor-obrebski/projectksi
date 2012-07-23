.. _web-deps:

WebDeps
=========

web_deps.py

Copyright © 2012 Nando Florestan

License: BSD

The problem: script and CSS linking in composite pages
======================================================

If you develop web applications in Python, and if sometimes you compose a page
out of fragments defined in various templates or functions, you may have asked
yourself how to best factor the importing of stylesheets and
javascript libraries. It feels wrong to use a javascript library in a
template that consubstantiates a page fragment while declaring the
<script> imports in another template.

There are 2 sides to this problem.
Worst of all is not declaring a library that is needed, 'cause then your
page does not work. But almost as bad is declaring everything you
might ever need in your master template -- because then, pages that don't need
heavy javascript libraries will be unnecessarily heavy and slow.

A solution is needed that allows you to first register everything you use,
then on each specific template or view declare what you need right there,
and the solution would generate the HTML imports, without repeating them.

We also must keep in mind that the order matters. For instance, jquery.ui
depends on jquery; and CSS has inheritance, so we need to link stylesheets
in the correct order.

The solution should also work with
any web framework and any templating language.

My solution: WebDeps
====================

The following classes solve the described problem.
First of all, while you configure the application, you declare the files
that might be imported:

.. code-block:: python

    deps = WebDeps()
    deps.lib('jquery', url="/static/lib/jquery-1.7.1.min.js")
    deps.lib('deform', url="/static/lib/deform.js",
        deps='jquery, jquery.ui')

The first argument to lib() -- and in fact to the other methods, too --
is a simple name for you to refer to the item later on.

As you can see, we can declare that deform.js depends on jquery and jquery.ui.
For more than one dependency, you just provide a comma-separated string::

    deps='jquery, jquery.ui'

What about CSS stylesheets? Just call css() instead of lib():

.. code-block:: python

    deps.css('jquery.ui', url='/static/css/jquery.ui.css')
    deps.css('deform', url="/deform/css/form.css", deps='jquery.ui')

They, too, can depend on other stylesheets, which are then output first.

Often javascript libraries work together with certain CSS stylesheets.
So we have a notion of a *package*:

.. code-block:: python

    deps.package('deform', libs='deform', css='deform',
         script='alert("Spam!");', deps='another_package')

A package is a special kind of dependency. It can refer to
scripts, stylesheets, other packages, and even contain some javascript code.

The above package declaration allows you to later say
"I need the 'deform' package here', and the system will output
the deform javascript library, CSS stylesheet, all their dependencies, and
some javascript code.

When everything needed by the web application has been declared, you need to
call close() to obtain a class that you will use on your pages::

    PageDeps = deps.close()

This ends initialization time. We are done with the registry.

But web servers are usually threaded and we cannot confuse the needs of
one page being served with another's. So now, for each new request,
make sure your web framework instantiates a PageDeps, and make it available to
controllers and templates. For instance, in the Pyramid web framework:

.. code-block:: python

    def on_new_request(event):
        event.request.deps = PageDeps()
    from pyramid.events import NewRequest
    # "config" below is assumed to be an instance of a
    # pyramid.config.Configurator object
    config.add_subscriber(on_new_request, NewRequest)

After that, controller/view code -- as well as templates, in some more
powerful templating languages -- can easily access a per-request
PageDeps instance and do this kind of thing:

.. code-block:: python

    # Use just one library:
    request.deps.lib('jquery')
    # Use 2 or more libraries:
    request.deps.lib(('jquery.ui, deform'))
    # Use a couple of stylesheets:
    request.deps.css('global, specific')
    # Or maybe import several stylesheets and javascript libraries at once:
    request.deps.package('deform')
    # You can also add ad hoc script fragments:
    request.deps.script('alert("Bruhaha!");')

A file can be requested more than once, but it will appear in the HTML
output only once and in the correct order.

Finally, we must deliver the HTML output. We shall use the best practice of
putting the CSS stylesheets at the top of the page and all the javascript
at the bottom of the page, near </body>. So, in your master template,
firstly include this inside the <head> element::

    ${Markup(request.deps.top_output)}

...where "Markup" is whatever function your templating language uses to
mark a string as a literal, so it won't be escaped.
"Markup" is from Genshi. In Chameleon you would say::

    ${structure: request.deps.top_output}

OR you can say "deps.css.tags" to the same effect: outputting the stylesheets.

Secondly include this just before the </body> tag::

    ${Markup(request.deps.bottom_output)}

Alternatively, use "deps.lib.tags" and "deps.script.tags".

You can also simply get lists of URLs (already sorted)::

    request.deps.css.urls
    request.deps.lib.urls

In short
========

There are 4 moments that should never be confused:

* Declaration of all available libs and stylesheets (and their proper order), done as the web server starts, with the WebDeps class;
* In the scope of one request, instantiation of a PageDeps;
* Declaration of what is needed by the current request;
* Output.

Deployment: Alternative URLs
============================

During development, for debugging, I like to use an uncompressed version
of jquery (a javascript library). But in production I like to use a CDN
(Content Delivery Network) for speed. And if the CDN stops working, I like to
have a third compressed version ready on my server.

These are 3 different URLs jquery.js might be served from. web_deps supports
this choice by letting you declare any and all URLs,
then letting you choose one in your configuration file.

How do you declare more than one URL? Well, the system stores any
keyword arguments you pass to lib() and css():

.. code-block:: python

    deps.lib('jquery', prod="/static/lib/jquery-1.7.1.min.js",
        dev="/static/lib/jquery-1.7.1.js",
        cdn='http://google.com/some/address/jquery-1.7.1.min.js')

Now the system has 3 URLs to choose from. Which will be in effect? Well, you
also provide a callable, that returns the desired URL, to the
WebDeps constructor as a "url_provider" keyword argument.
Its default implementation is this::

    url_provider=lambda resource: resource.url

Evidently the above implementation gets the URL from the "url" argument.
But that could be "dev", "prod", "cdn" or whatever you like.
It is trivial for you to put this decision in a configuration file.
Suppose the configuration file says::

    web_deps.url_choice = cdn

All you have to do is:

.. code-block:: python

    # Read the string from the configuration file, providing a default
    choice = settings.get('web_deps.url_choice', 'prod')
    # Pass a url_provider callable to the WebDeps constructor
    def url_provider(resource):
        return getattr(resource, choice, None) or resource.url
    deps = WebDeps(url_provider=url_provider)

This way you can declare the libraries once in your code, in a centralized
place, but easily configure which one is actually used based on
the deployment configuration.

The above implementation will look for a 'prod' argument if the currently
configured choice is 'prod'. If not found, it will look for a 'url' argument.
This lets you provide either the 3 alternative URLs, or just one.

Why would you provide only one URL? Not every file is provided by a CDN and
not every javascript library is worth compressing. The reality we have
experienced is we either want 3 alternative URLs, or just one. Anyway,
suit yourself in your own url_provider implementation.

Advantages over page_deps
=========================

This module, "web_deps", is superior to my previous attempt, called
"page_deps", in the following ways:

* Dependency declarations may be done in any order.
  You can declare that *b* depends on "a", then declare what "a" is later.
* Some computation occurs when close() is called. From this moment on,
  trying to add a dependency throws an exception.
* The general dependency problem has been solved in the base classes
  Dependency and DepsRegistry, which can be reused in other scenarios.
  The specific web problem is solved by inheriting from these superclasses.
* Therefore, more code is reused between javascript and CSS dependencies.
* Now packages can depend on other packages, too.
* In page_deps stylesheets didn't really have dependencies, just priority.
  This was a mistake.
* Results are cached so your web application runs faster.
* Much better user API.
* The code is better organized.
* It has more comprehensive unit tests.

Questions?
==========

For feature requests and bug reports, please visit
http://code.google.com/p/bag/issues/list
