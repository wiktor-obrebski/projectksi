from projectksi.core import plugins
from projectksi.models import tables
from projectksi.models.tables import DBSession

class Test(object):
    pass

class Module(plugins.PluginAbstract):

    def name(self):
        #char = DBSession.query(tables.Character).first()
        return "testing_module"

    def description(self,config):
        return 'Sample module created for tests'
