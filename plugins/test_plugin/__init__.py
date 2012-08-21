from projectksi.core import plugins
from projectksi.models import tables
from projectksi.models.tables import DBSession

class Plugin(plugins.PluginAbstract):

    def unique_name(self):
        #char = DBSession.query(tables.Character).first()
        return "testing_plugin_#@%#@%"

    def readable_name(self):
        return "Testing plugin"

    def description(self):
        return 'Sample plugin created for tests'
