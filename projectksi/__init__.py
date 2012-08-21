from pyramid.config import Configurator
from projectksi.core.plugins import PluginsManager
from projectksi.core import webdeps_extend
from projectksi.core import jinja2_extend
from sqlalchemy import engine_from_config
from projectksi.models.tables import DBSession
import logging

def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    config = Configurator(settings=settings, root_factory=get_root)
    plugins_manager = PluginsManager(config)

    #initialize sqlalchemy
    engine = engine_from_config(settings, 'sqlalchemy.')
    DBSession.configure(bind=engine)

    init_webdeps(config)

    config.add_static_view('static', 'static', cache_max_age=3600)
    #config.add_route('home', '/')
    config.scan()

    return config.make_wsgi_app()

def init_webdeps(config):
    """ This function initalize WebDeps library, depending on url_choice configure value, next
    it preparing jinja2 functions that will make possible choosing css, jss and less relations
    inside specific template.
    """
    url_choice = config.registry.settings.get('web_deps.url_choice', 'production')
    PageDeps = webdeps_extend.initialize_web_deps(url_choice)
    config.registry.PageDeps = PageDeps

    jinja_env = config.get_jinja2_environment()
    jinja_env.globals['include_css'] = jinja2_extend.WebDepsIncluder('css')
    jinja_env.globals['include_js'] = jinja2_extend.WebDepsIncluder('lib')
    jinja_env.globals['include_less'] = jinja2_extend.WebDepsIncluder('less')

class Resource(dict):
    pass

def get_root(request):
    return Resource( {'a' : Resource() } )