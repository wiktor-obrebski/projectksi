from pyramid.config import Configurator
from projectksi import core

def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    config = Configurator(settings=settings)

    url_choice = settings.get('web_deps.url_choice', 'prod')
    PageDeps = core.initialize_web_deps(url_choice)
    config.registry.PageDeps = PageDeps

    config.add_static_view('static', 'static', cache_max_age=3600)
    config.add_route('home', '/')
    config.scan()
    return config.make_wsgi_app()
