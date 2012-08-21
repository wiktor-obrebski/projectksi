from projectksi.core import plugins
from projectksi.models import tables
from projectksi.models.tables import DBSession
from pyramid.response import Response
from pyramid.view import view_config
from pyramid_viewscomposer.decorators import compose_view_config

@compose_view_config(route_name='test', renderer='test_template.jinja2')
def hello_world(request):
    return { 'a' : 123, 'project' : 'something' }

@compose_view_config(route_name='test')
def hello_world2(request):
    return { 'a2' : 123, 'project2' : 'something' }

class Plugin(plugins.PluginAbstract):

    def unique_name(self):
        #char = DBSession.query(tables.Character).first()
        return "testing_plugin_#@%#@%"

    def readable_name(self):
        return "Testing plugin"

    def description(self):
        return 'Sample plugin created for tests'
        #config.add_view(hello_world, route_name='test')

    def includeme(self,config):
        config.add_route('test', '/test')
        config.scan()
