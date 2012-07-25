from projectksi.core.vendor.bag import web_deps

class WebDeps(web_deps.WebDeps):
    """ Override default WebDeps object, to add supporting
    for LESS link rel.
    """
    def __init__(self, url_provider=lambda resource: resource.url):
        super(WebDeps, self).__init__(url_provider=url_provider)
        self.less = web_deps.WebDepsRegistry(url_provider=url_provider,
                                             tag_format='<link rel="stylesheet/less" type="text/css" href="{}" />')

    def close(self):
        super(WebDeps, self).close()
        self.less.close()

        def factory():
            pd = web_deps.PageDeps(self.lib, self.css, self.package)
            pd.less = web_deps.PageDepsComponent(self.less)
            return pd
        return factory

def initialize_web_deps(url_choice):
    """ *initialize_web_deps* method initialize all css, less and js dependency list,
    depending on *web_deps.url_choice* setting. it return PageDeps object, that should
    be used to register specific dependency in specific views.
    """

    # Pass a url_provider callable to the WebDeps constructor
    def url_provider(resource):
        return getattr(resource, url_choice, None) or resource.url

    deps = WebDeps(url_provider=url_provider)

    #css dependencies
    deps.lib('less', url="/static/js/less-1.3.0.min.js")
    deps.lib('jquery', develop="/static/js/jquery-1.7.2.js", production="/static/js/jquery-1.7.2.min.js")
    deps.lib('bootstrap', develop="/static/js/bootstrap.js", production="/static/js/bootstrap.min.js")

    #less dependencies
    deps.less('projectksi', url='static/css/projectksi.less')

    #css dependencies
    deps.css('bootstrap', develop="/static/css/bootstrap.css", production="/static/css/bootstrap.min.css")
    deps.css('bootstrap-responsive', develop="/static/css/bootstrap-responsive.css",
             production="/static/css/bootstrap-responsive.min.css")
    PageDeps = deps.close()
    return PageDeps