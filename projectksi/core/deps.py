""" In this module we have all code related with page deps - js, css and less loading.
"""

import squeezeit
import yaml
import os
import logging
import subprocess
from os.path import relpath
from os.path import splitext
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
    coffee_side = s.get('projectksi.web_deps.coffee_compiler.side', 'server')

    config_path = s.get('projectksi.web_deps.squeezeit.config', '../config.yaml')

    stream = open(config_path, 'r')
    dep_pathes = yaml.load(stream)
    stream.close()

    if less_side == 'server':
        compile_less_server_side(config, dep_pathes)
    elif less_side == 'client':
        compile_less_client_side(config, dep_pathes)

    if coffee_side == 'client':
        compile_coffee_script(config, dep_pathes, False)
        debug_watch_coffee_files(config, dep_pathes)
    elif coffee_side == 'server':
        compile_coffee_script(config, dep_pathes, False)

    if squeezeit_enabled:
        init_squeezeit(config, dep_pathes)
    else:
        init_raw_deps(config, dep_pathes)


def compile_coffee_file(compiler_path, dep_pathes, file_path, source_maps=True):
    """ This funtion compile *file_path* by using system coffee redux compiler getted
    from *compiler_path*. It will generate source maps for compiled files if *source_maps*
    flags is True. Source maps will have name like original file + '.map'.
    """
    org_file_path = file_path
    if file_path in monitor_dictionary:
        act_mtime = os.stat(file_path).st_mtime
        if act_mtime <= monitor_dictionary[file_path]:
            return

    output_dir = dep_pathes['coffeeCompileOutput']
    coffee_base_dir = dep_pathes['coffee']

    print('recompile "%s" coffee file.' % relpath(file_path, coffee_base_dir))

    #os.path.realpath is used for generating source maps process purposes.
    js_cmds = [compiler_path, '-i', file_path]

    file_rel_path = relpath(file_path, coffee_base_dir)
    #-o option not working for now, so we left it to fix later
    js_cmds.extend(['--js'])  #, '-o', output_dir + file_rel_path])

    js_output, err = subprocess.Popen(js_cmds, stdout=subprocess.PIPE,
                                      stderr=subprocess.PIPE).communicate()
    new_path = output_dir + file_rel_path
    new_path = splitext(new_path)[0] + '.js'
    new_path_dir = os.path.dirname(new_path)
    if not os.path.exists(new_path_dir):
        os.mkdir(new_path_dir)

    stream = open(new_path, 'bw+')
    if(source_maps):
        line = '//@ sourceMappingURL=%s.map\n' % os.path.basename(new_path)
        stream.write(line.encode('utf-8'))
    stream.write(js_output)
    stream.close()

    if(source_maps):
        #we need run compiler in target directory to generate good pathes in source-maps
        file_path = relpath(file_path, new_path_dir)
        sm_cmds = [compiler_path, '-i', file_path]
        sm_cmds.extend(['--source-map'])
        sm_output, err = subprocess.Popen(sm_cmds, stdout=subprocess.PIPE, cwd=new_path_dir,
                                      stderr=subprocess.PIPE).communicate()
        stream = open(new_path + '.map', 'bw+')
        stream.write(sm_output)
        stream.close()

    monitor_dictionary[org_file_path] = os.stat(org_file_path).st_mtime


monitor_dictionary = {}


def debug_watch_coffee_files(config, dep_pathes):
    """ It will create new thread that will be checking in interval of one second
    for changes in our coffee files - and recompile it to js when their changed/
    """
    s = config.registry.settings
    compiler_path = s.get('projectksi.web_deps.coffee_compiler.path', '__coffee')

    files_to_monitor = []
    bundles = [f for f in os.listdir(dep_pathes['bundles']) if f.endswith('.yaml')]
    for f in bundles:
        stream = open('/'.join([dep_pathes['bundles'], f]), 'r')
        data = yaml.load(stream)
        stream.close()
        if 'coffee' in data['includes']:
            for filename in data['includes']['coffee']:
                file_path = dep_pathes['coffee'] + filename
                files_to_monitor.append(file_path)

    import threading

    class MyThread(threading.Thread):

        def run(self):
            import time
            while(True):
                for file_path in files_to_monitor:
                    compile_coffee_file(compiler_path, dep_pathes, file_path, source_maps=True)
                time.sleep(1)

    thread = MyThread()
    #to not ignore Ctrl+C in parent thread
    thread.daemon = True
    thread.start()


def compile_coffee_script(config, dep_pathes, include_source_maps=False):
    """ Run coffee-script compiler to compile all coffee scripts,
    add them to "include_compiled_js" list and eventually generate source maps for them.
    """
    include_js = []
    s = config.registry.settings
    compiler_path = s.get('projectksi.web_deps.coffee_compiler.path', '__coffee')

    bundles = [f for f in os.listdir(dep_pathes['bundles']) if f.endswith('.yaml')]
    for f in bundles:
        stream = open('/'.join([dep_pathes['bundles'], f]), 'r')
        data = yaml.load(stream)
        stream.close()
        if 'coffee' in data['includes']:
            for filename in data['includes']['coffee']:
                file_path = dep_pathes['coffee'] + filename
                try:
                    compile_coffee_file(compiler_path, dep_pathes, file_path, include_source_maps)
                except OSError:
                    print('You need set proper coffee compiler in "%s" configuration entry.' %
                            'projectksi.web_deps.coffee_compiler.path')

                    import sys
                    sys.exit(-1)

                js_static_path = relpath(dep_pathes['coffeeCompileOutput'], './projectksi')
                file_rel_path = relpath(file_path, dep_pathes['coffee'])
                file_rel_path = splitext(file_rel_path)[0] + '.js'
                include_js.append('/'.join([js_static_path, file_rel_path]))

    config.registry.include_compiled_js = include_js


def compile_less_server_side(config, dep_pathes):
    """ Use LessCSS to compile less files in css static directory
    """
    try:
        less_dir = dep_pathes['less']
        output_dir = dep_pathes['lessCompileOutput']
        LessCSS(media_dir=less_dir, based=False,
                compressed=False, output_dir=output_dir)
    except OSError:
        logging.warning('Can not compiling LESS - lessc not founded in system.')


def compile_less_client_side(config, dep_pathes):
    """ Add *less-1.3.0.min.js* to js included (for jinja template) and
    and register *.less files (with names like from 'css' path from *dep_pathes*, but
    with .less extenstion) for later use in jinja template.
    """
    if not hasattr(config.registry, 'include_js'):
        config.registry.include_js = []

    js_project_path = relpath(dep_pathes['javascript'], './projectksi')
    less_project_path = relpath(dep_pathes['less'], './projectksi')

    config.registry.include_js.append('/'.join([js_project_path, 'less-1.3.0.min.js']))

    rel_list = rel_dir_list(dep_pathes['less'], 'less')
    include_less = ['/'.join([less_project_path, f]) for f in rel_list]

    rel_less = relpath(dep_pathes['less'], './projectksi')

    less_list = load_file_names_from_yaml(dep_pathes['bundles'], 'less')
    less_list = ['/'.join([rel_less, f]) for f in less_list]

    config.registry.include_less = [f for f in include_less
                                    if f in less_list]


def init_raw_deps(config, dep_pathes):
    """ Checking directories listed in *dep_pathes* for css and js files.
    Next create two static views - "develop-css" and "develop-js" and serve
    this directories. Prepare list of js and css files to include later by jinja
    templates. Ignore css files that was before include in "LESS" version.
    Should be used only in development.
    """
    for key in ['css', 'javascript', 'less', 'coffee']:
        path = os.path.relpath(dep_pathes[key], './projectksi')
        config.add_static_view('develop-%s' % key, path, cache_max_age=0)

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

    css_static_path = relpath(dep_pathes['css'], './projectksi')
    include_css = ['/'.join([css_static_path, f]) for f in css]
    include_css = [f for f in include_css if splitext(f)[0] + '.less' not in include_less]
    config.registry.include_css = include_css

    js_static_path = relpath(dep_pathes['javascript'], './projectksi')
    include_js.extend(['/'.join([js_static_path, f]) for f in js])
    if hasattr(config.registry, 'include_compiled_js'):
        include_js.extend(config.registry.include_compiled_js)
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
    #os.remove(tmp_config_path)

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

    rel_publish_dir = relpath(publish_path, './projectksi')

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
        outputList.extend([relpath(f, dir_name) for f in fit_files])
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


squeezeit_loadbundles = squeezeit.loadbundles


def loadbundles(configfile, config):
    """ This is small hack - we override default *loadbundles* method from squeezeit
    library to learn it what to do with LESS and COFFEE entries. This entries Should
    be moved to CSS (for LESS) and JS(for COFFEE) entries, with changed extension
    and target directory.
    """
    data = squeezeit_loadbundles(configfile, config)
    rel_less = relpath(config['lessCompileOutput'], config['css'])
    rel_coffee = relpath(config['coffeeCompileOutput'], config['javascript'])
    for key, bundle in data.items():
        if 'less' in bundle['includes']:
            for lesspath in bundle['includes']['less']:
                filename = os.path.splitext(lesspath)[0]
                data[key]['includes']['css'].append('%s/%s.css' % (rel_less, filename))
        if 'coffee' in bundle['includes']:
            for coffeepath in bundle['includes']['coffee']:
                filename = os.path.splitext(coffeepath)[0]
                data[key]['includes']['javascript'].append('%s/%s.js' % (rel_coffee, filename))
    return data

squeezeit.loadbundles = loadbundles
