from projectksi.core.vendor.bag import web_deps

definitions = {
    'js'    :   {
        'less'      : '/static/js/less-1.3.0.min.js',
        'jquery'    : ('/static/js/jquery-1.7.2.js', '/static/js/jquery-1.7.2.min.js'),
        'bootstrap' : ('/static/js/bootstrap.js', '/static/js/bootstrap.min.js')
    },
    'less'  :   {
        'projectksi': 'static/css/projectksi.less'
    },
    'css'   :   {
        'bootstrap' : ('/static/css/bootstrap.css', '/static/css/bootstrap.min.css'),
        'bootstrap-responsive' : ('/static/css/bootstrap-responsive.css', '/static/css/bootstrap-responsive.min.css')
    }
}

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

    def load_deps(dep_type,callback):
        for name, value in definitions[dep_type].items():
            if type(value) is str:
                callback(name, url=value)
            else:
                callback(name, develop=value[0], production=value[1])

    #js dependencies
    load_deps('js', deps.lib)
    #less dependencies
    load_deps('less', deps.less)
    #css dependencies
    load_deps('css', deps.css)

    PageDeps = deps.close()
    return PageDeps