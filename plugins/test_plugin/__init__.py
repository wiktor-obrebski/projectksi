from projectksi.core import plugins
from pyramid_viewscomposer.decorators import compose_view_config


@compose_view_config(route_name='test', renderer='test_template.jinja2')
def hello_world(request):
    return {'a': 123, 'project': 'something'}


@compose_view_config(route_name='test')
def hello_world2(request):
    return {'a2': 123, 'project2': 'something'}


class Plugin(plugins.PluginAbstract):

    def unique_name(self):
        #char = DBSession.query(tables.Character).first()
        return "testing_plugin_#@%#@%"

    def readable_name(self):
        return "Testing plugin"

    def description(self):
        return 'Sample plugin created for tests'

    def depending(self):
        """ tuple of unique_name without which this particular plugin
         can not working
        """
        return ()

    def services_depending(self):
        """ tuple of service keys without which this particular plugin
        can not working. This will be visible for debug purposes.
        """
        return ('non-exist-service1', 'non-exist-service2')

    instances = 0

    def test_message_service(self):
        class SampleService(object):
            def __init__(self2):
                self.instances = self.instances + 1

            def test_message(self2, value):
                return ("this is test message that will be generated when "
                        "anybody call 'test-message' service, with arg: '%s'. "
                        "Generated %s time." % (value, self.instances))
        return SampleService()

    def url_service(self):
        def popular_url(name):
            if name == "docs":
                return "http://docs.projectksi.com/"
            elif name == "site":
                return "http://projectksi.com/"
            elif name == "secret":
                return "http://my-secret-url.com/"
        return popular_url


    def includeme(self, config, service_locator):
        config.add_route('test', '/test')
        service_locator.set('test-message-generator',
                             self.test_message_service)
        service_locator.set('url-service', self.url_service)

        url_service = service_locator.get('url-service')
        print(url_service("docs"))
        print(url_service("site"))
        print(url_service("secret"))

        #this code can be called from any other plugin.
        #class SampleService will be generated
        #only when anybody really call "sl.get" method - and only one time.
        gen = service_locator.get('test-message-generator')
        print(gen.test_message('666'))
        gen2 = service_locator.get('test-message-generator')
        print(gen2.test_message('777'))
        gen3 = service_locator.get('test-message-generator')
        print(gen3.test_message('888'))
        config.scan()
