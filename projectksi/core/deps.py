""" In this module we have all code related with page deps - js, css and less loading.
"""

import squeezeit
import yaml
import os
import os.path
from pyramid.settings import asbool


def init_deps(config):
    """ if config *squeezeit.enabled* directive is set to true - it will call *init_squeezeit*
    method - otherwise *init_raw_deps*
    """
    squeezeit_enabled = asbool(config.registry.settings.get('squeezeit.enabled', False))
    if squeezeit_enabled:
        init_squeezeit(config)
    else:
        init_raw_deps(config)


def rel_dir_list(dir_name, ext):
    """ Returns all files with extension *ext* from directory, recursively *dir_name*.
    Pathes will be relative to *dir_name*.
    """
    outputList = []
    for root, dirs, files in os.walk(dir_name):
        fit_files = [('/'.join([root, f])) for f in files if f.endswith('.' + ext)]
        outputList.extend([os.path.relpath(f, dir_name) for f in fit_files])
    return outputList


def init_raw_deps(config):
    """ Checking directories listed in *"squeezeit.config"* for css and js files.
    Next create two static views - "develop-css" and "develop-js" and serve
    this directories. Prepare list of js and css files to include later by jinja
    templates. Should be used only in development.

    It use *squeezeit.config* config directive path to find folders with css and js
    files.
    """
    config_path = config.registry.settings.get('squeezeit.config', '../config.yaml')

    stream = open(config_path, 'r')
    data = yaml.load(stream)
    stream.close()

    css_static_path = os.path.relpath(data['css'], './projectksi')
    js_static_path = os.path.relpath(data['javascript'], './projectksi')
    config.add_static_view('develop-css', css_static_path, cache_max_age=3600)
    config.add_static_view('develop-js', js_static_path, cache_max_age=3600)

    config.registry.include_css = ['/'.join([css_static_path, f]) for f in rel_dir_list(data['css'], 'css')]
    config.registry.include_js = ['/'.join([js_static_path, f]) for f in rel_dir_list(data['javascript'], 'js')]


def init_squeezeit(config):
    """ By using *squeezeit* library - minimize, pack and combine js/css files to bundles.
    Next check their names and prepare it to later include in jinja templates.
    Prepare static view *static* that will serve files from squeezeit output directory.
    """
    #Confirm the command line arguments exist
    config_path = config.registry.settings.get('squeezeit.config', '../config.yaml')
    prefered_version = config.registry.settings.get('squeezeit.prefered_version', 'gz')

    #Start the processing
    squeezeit.compress(config_path)

    stream = open(config_path, 'r')
    data = yaml.load(stream)
    stream.close()
    publish_path = data['output']

    include_css = []
    include_js = []

    yaml_files = [f for f in os.listdir(publish_path) if f.endswith('.yaml')]
    for f in yaml_files:
        stream = open('/'.join([publish_path, f]), 'r')
        data = yaml.load(stream)
        stream.close()
        if 'css' in data['ksipack']:
            include_css.append(data['ksipack']['css']['output'][prefered_version])
        if 'javascript' in data['ksipack']:
            include_js.append(data['ksipack']['javascript']['output'][prefered_version])

    rel_publish_dir = os.path.relpath(publish_path, './projectksi')

    config.registry.include_css = ['/'.join([rel_publish_dir, f]) for f in include_css]
    config.registry.include_js = ['/'.join([rel_publish_dir, f]) for f in include_js]

    config.add_static_view('static', rel_publish_dir, cache_max_age=3600)
