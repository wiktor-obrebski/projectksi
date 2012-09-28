from pyramid.config import Configurator
from projectksi.core.plugins import PluginsManager
from sqlalchemy import engine_from_config
from projectksi.models.tables import DBSession
from projectksi.core import deps


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    config = Configurator(settings=settings)

    plugins_manager = PluginsManager(config)
    config.registry.plugins = plugins_manager
    deps.init_deps(config)

    #initialize sqlalchemy
    engine = engine_from_config(settings, 'sqlalchemy.')
    DBSession.configure(bind=engine)

    config.add_static_view('img', 'static/img', cache_max_age=3600)
    config.add_route('home', '/')
    config.scan()

    return config.make_wsgi_app()
