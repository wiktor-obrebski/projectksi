import inspect
from importlib import import_module

class PluginAbstract(object):
    """ Base class that should be implemented in all plugins added to game. It is
    provided few methods and information that give our more control for plugins management.
    """

    def name(self):
        """ Plugin base name
        """
        raise NotImplementedError()

    def description(self):
        """ Plugin description, should have human readable info about what exacly this plugin divmod
        """
        raise NotImplementedError()

    def __call__(self,config):
        print(self.name())

class PluginsManager(object):
    modules={}

    def __init__(self, config):
        self.config = config
        config.action('register_plugins', self._register_plugins, args=(config,) )

    def _register_plugins(self, config):
        """ This method looking for 'projectksi.plugins' configuration entry.
        If it exist, it should contains modules list that will be treated as
        projectksi plugins modules. Method will be looking for class derived
        from "PluginAbstract" class, if it will not found it, exception will be
        raised.
        """
        p_str = config.registry.settings.get('projectksi.plugins', '' )
        p_list = p_str.split()
        for plugin_name in p_list:
            mod = import_module(plugin_name)

            classes = inspect.getmembers(mod, inspect.isclass)
            plugin_classes = [c[1] for c in classes if issubclass(c[1], PluginAbstract)]
            if(len(plugin_classes) > 1):
                raise Exception('More that one class derivered'
                                ' by PluginAbstract founded in "%s" plugin.' % plugin_name)
            elif(len(plugin_classes) == 0):
                raise Exception('Plugins "%s" need have one class derivered '
                                'by PluginAbstract in his __init__.py file.' % plugin_name)
            module_class = plugin_classes[0]

            module = module_class()
            self.modules[module.name()] = module

        print(self.modules)
