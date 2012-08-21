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

    instances = 0
    def test_message_service(self):
        class SampleService(object):
            def __init__(self2):
                self.instances = self.instances + 1

            def test_message(self2, value):
                return ("this is test message that will be generated when anybody call "
                        "'test-message' service, with arg: '%s'. "
                        "Generated %s time." % (value, self.instances))
        return SampleService()

    def includeme(self,config,service_locator):
        config.add_route('test', '/test')
        service_locator.set('test-message-generator', self.test_message_service)

        #this code can be called from any other plugin. class SampleService will be generated
        #only when anybody really call "sl.get" method - and only one time.
        gen = service_locator.get('test-message-generator')
        print(gen.test_message('666'))
        gen2 = service_locator.get('test-message-generator')
        print(gen2.test_message('777'))
        gen3 = service_locator.get('test-message-generator')
        print(gen3.test_message('888'))
        config.scan()
