""" In this module we have all code related with page deps - js, css and less loading.
"""

import squeezeit
import yaml
import os
import os.path
import logging
from pyramid.settings import asbool
from lesscss import LessCSS


def init_deps(config):
    """ if config *squeezeit.enabled* directive is set to true - it will call *init_squeezeit*
    method - otherwise *init_raw_deps*. When *projectksi.web_deps.less_compiler.side* directive
    is set to 'server' will call *compile_less_server_side*, else *compile_less_client_side*
    """
    s = config.registry.settings
    squeezeit_enabled = asbool(s.get('projectksi.web_deps.squeezeit.enabled', False))
    less_side = s.get('projectksi.web_deps.less_compiler.side', 'server')

    config_path = s.get('projectksi.web_deps.squeezeit.config', '../config.yaml')

    stream = open(config_path, 'r')
    dep_pathes = yaml.load(stream)
    stream.close()

    if less_side == 'server':
        compile_less_server_side(config, dep_pathes)
    elif less_side == 'client':
        compile_less_client_side(config, dep_pathes)

    if squeezeit_enabled:
        init_squeezeit(config, dep_pathes)
    else:
        init_raw_deps(config, dep_pathes)


def compile_less_server_side(config, dep_pathes):
    """ Use LessCSS to compile less files in css static directory
    """
    try:
        LessCSS(media_dir=dep_pathes['css'], based=False, compressed=False)
    except OSError:
        logging.warning('Can not compiling LESS - lessc not founded in system.')


def compile_less_client_side(config, dep_pathes):
    """ Add *less-1.3.0.min.js* to js included (for jinja template) and
    and register *.less files (with names like from 'css' path from *dep_pathes*, but
    with .less extenstion) for later use in jinja template.
    """
    if not hasattr(config.registry, 'include_js'):
        config.registry.include_js = []

    js_project_path = os.path.relpath(dep_pathes['javascript'], './projectksi')
    css_project_path = os.path.relpath(dep_pathes['css'], './projectksi')

    config.registry.include_js.append('/'.join([js_project_path, 'less-1.3.0.min.js']))

    rel_list = rel_dir_list(dep_pathes['css'], 'less')
    include_less = ['/'.join([css_project_path, f]) for f in rel_list]

    splitext = os.path.splitext
    relpath = os.path.relpath
    rel_css = relpath(dep_pathes['css'], './projectksi')

    css_list = load_file_names_from_yaml(dep_pathes['bundles'], 'css')
    css_list = ['/'.join([rel_css, f]) for f in css_list]

    config.registry.include_less = [f for f in include_less
                                    if splitext(f)[0] + '.css' in css_list]


def init_raw_deps(config, dep_pathes):
    """ Checking directories listed in *dep_pathes* for css and js files.
    Next create two static views - "develop-css" and "develop-js" and serve
    this directories. Prepare list of js and css files to include later by jinja
    templates. Ignore css files that was before include in "LESS" version.
    Should be used only in development.
    """
    css_static_path = os.path.relpath(dep_pathes['css'], './projectksi')
    js_static_path = os.path.relpath(dep_pathes['javascript'], './projectksi')
    config.add_static_view('develop-css', css_static_path, cache_max_age=0)
    config.add_static_view('develop-js', js_static_path, cache_max_age=0)

    css = load_file_names_from_yaml(dep_pathes['bundles'], 'css')
    js = load_file_names_from_yaml(dep_pathes['bundles'], 'javascript')

    try:
        include_less = config.registry.include_less
    except AttributeError:
        include_less = []

    try:
        include_js = config.registry.include_js
    except AttributeError:
        include_js = []

    splitext = os.path.splitext

    include_css = ['/'.join([css_static_path, f]) for f in css]
    include_css = [f for f in include_css if splitext(f)[0] + '.less' not in include_less]
    config.registry.include_css = include_css

    include_js.extend(['/'.join([js_static_path, f]) for f in js])
    config.registry.include_js = include_js


def init_squeezeit(config, dep_pathes):
    """ By using *squeezeit* library - minimize, pack and combine js/css files to bundles.
    Next check their names and prepare it to later include in jinja templates.
    Prepare static view *static* that will serve files from squeezeit output directory.
    """
    s = config.registry.settings
    prefered_version = s.get('projectksi.web_deps.squeezeit.prefered_version', 'gz')
    config_path = s.get('projectksi.web_deps.squeezeit.config', '../config.yaml')

    #Start the processing
    squeezeit.compress(config_path)

    publish_path = dep_pathes['output']

    try:
        include_css = config.registry.include_css
    except AttributeError:
        include_css = []
    try:
        include_js = config.registry.include_js
    except AttributeError:
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


def rel_dir_list(dir_name, ext):
    """ Returns all files with extension *ext* from directory, recursively *dir_name*.
    Pathes will be relative to *dir_name*.
    """
    outputList = []
    for root, dirs, files in os.walk(dir_name):
        fit_files = [('/'.join([root, f])) for f in files if f.endswith('.' + ext)]
        outputList.extend([os.path.relpath(f, dir_name) for f in fit_files])
    return outputList


def load_file_names_from_yaml(directory, directive):
    """ Looking for "*.yaml" file in *dir* and load their files name from *directive*
    """
    yaml_files = [f for f in os.listdir(directory) if f.endswith('.yaml')]
    pathes = []
    for f in yaml_files:
        stream = open('/'.join([directory, f]), 'r')
        try:
            pathes.extend(yaml.load(stream)['includes'][directive])
        except KeyError:
            pass
        stream.close()
    return pathes
