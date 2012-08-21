import inspect
from importlib import import_module

class PluginAbstract(object):
    """ Base class that should be implemented in all plugins added to game. It is
    provided few methods and information that give our more control for plugins management.
    """

    def unique_name(self):
        """ Plugin base name
        """
        raise NotImplementedError()

    def readable_name(self):
        """ Human readable plugin name, for printing pursposes
        """
        return self.unique_name()

    def name(self):
        """ Only shortcut to "readable_name" method
        """
        return self.readable_name()

    def description(self):
        """ Plugin description, should have human readable info about what exacly this plugin divmod
        """
        raise NotImplementedError()

    def __call__(self,config):
        print(self.name())

class PluginsManager(object):
    plugins={}

    def __init__(self, config):
        self.config = config
        self._register_plugins(config)
        #config.action('register_plugins', self._register_plugins, args=(config,), introspectables=(intr,) )

    def _register_plugins(self, config):
        """ This method looking for 'projectksi.plugins' configuration entry.
        If it exist, it should contains plugins list that will be treated as
        projectksi plugins plugins. Method will be looking for class derived
        from "PluginAbstract" class, if it will not found it, exception will be
        raised.
        """
        plugins = {}
        introspectables = []
        p_str = config.registry.settings.get('projectksi.plugins', '' )
        p_list = p_str.split()
        for plugin_path in p_list:
            mod = import_module(plugin_path)

            classes = inspect.getmembers(mod, inspect.isclass)
            plugin_classes = [c[1] for c in classes if issubclass(c[1], PluginAbstract)]
            if(len(plugin_classes) > 1):
                raise Exception('More that one class derivered'
                                ' by PluginAbstract founded in "%s" plugin.' % plugin_path)
            elif(len(plugin_classes) == 0):
                raise Exception('Plugins "%s" need have one class derivered '
                                'by PluginAbstract in his __init__.py file.' % plugin_path)
            plugin_class = plugin_classes[0]

            plugin = plugin_class()
            plugin_name = plugin.name()
            plugins[plugin_name] = plugin

            intr = config.introspectable(category_name='projectksi plugins',
                                 discriminator=( 'plugin', plugin_name ),
                                 title=('<%s>' % plugin.unique_name()),
                                 type_name='projectksi plugin')
            intr['name'] = plugin_name
            intr['description'] = plugin.description()

            introspectables.append(intr)

        config.action('apply_plugins', self._apply_plugins, args=(config, plugins),
                      introspectables=introspectables)

    def _apply_plugins(self, config, plugins):
        self.plugins = plugins