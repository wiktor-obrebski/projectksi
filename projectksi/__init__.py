from pyramid.config import Configurator
from projectksi.core.view_helpers import HelperRequest

def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    config = Configurator(settings=settings, request_factory=HelperRequest)
    config.add_static_view('static', 'static', cache_max_age=3600)
#    config.override_asset(to_override='projectksi:static/',
#                          override_with='projectksi:static/develop/')
    config.add_route('home', '/')
    config.scan()
    return config.make_wsgi_app()
