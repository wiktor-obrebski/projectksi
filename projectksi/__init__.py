from pyramid.config import Configurator
from projectksi.core.plugins import PluginsManager
from projectksi.core import webdeps_extend
from projectksi.core import jinja2_extend
from sqlalchemy import engine_from_config
from projectksi.models.tables import DBSession
import squeezeit
import yaml
import os


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    config = Configurator(settings=settings)
    plugins_manager = PluginsManager(config)
    config.registry.plugins = plugins_manager
    init_squeezeit(config)

    #initialize sqlalchemy
    engine = engine_from_config(settings, 'sqlalchemy.')
    DBSession.configure(bind=engine)

    #init_webdeps(config)

    config.add_static_view('static', 'static/publish', cache_max_age=3600)
    config.add_static_view('img', 'static/img', cache_max_age=3600)
    config.add_route('home', '/')
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


def init_squeezeit(config):
    #Confirm the command line arguments exist
    config_path = config.registry.settings.get('squeezeit.config', 'config.yaml')
    prefered_version = config.registry.settings.get('squeezeit.prefered_version', 'gz')

    #Start the processing
    squeezeit.compress(config_path)

    include_css = []
    include_js = []

    path = 'projectksi/static/publish'
    yaml_files = [f for f in os.listdir(path) if f.endswith('.yaml')]
    for f in yaml_files:
        stream = open("%s/%s" % (path, f), 'r')
        data = yaml.load(stream)
        if 'css' in data['ksipack']:
            include_css.append(data['ksipack']['css']['output'][prefered_version])
        if 'javascript' in data['ksipack']:
            include_js.append(data['ksipack']['javascript']['output'][prefered_version])

    config.registry.include_css = include_css
    config.registry.include_js = include_js
