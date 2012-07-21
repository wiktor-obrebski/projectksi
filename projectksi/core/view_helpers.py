from pyramid.request import Request

class StaticUrlDebug( object ):
    """ calling this class will find last
    dot in @url path and insert text: "min." after
    it - unless file name in url is in "exceptions" list
    """

    exceptions = [
        'projectksi.less',
        'less-1.3.0.min.js',
    ]
    def __call__(self, url):
        pos = url.rfind('/')
        if url[pos+1:] not in self.exceptions:
            pos = url.rfind('.')
            if pos > 0:
                return url[:pos] + '.min' + url[pos:]
        return url

class HelperRequest( Request ):
    """ We override default request object to give more functionality
    for python templates. Any method added there can be call in template
    by request.{method_name}.
    """

    def static_url(self, name):
        """ Override default static_url method to automatically generate "*.min*"
        names for static files
        """
        debug_mode = ('projectksi.debugmode' in self.registry.settings
                       and self.registry.settings['projectksi.debugmode'])

        result = super(HelperRequest, self).static_url(name)
        if not debug_mode:
            sud = StaticUrlDebug()
            result = sud(result)
        return result