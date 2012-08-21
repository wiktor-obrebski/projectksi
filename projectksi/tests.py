import unittest

from pyramid import testing
from projectksi.core.plugins import ServiceLocator

class ServiceLocatorTests(unittest.TestCase):
    def setUp(self):
        self.config = testing.setUp()

    def tearDown(self):
        testing.tearDown()

######### sl.has() tests #######

    def test_has_not_exists(self):
        sl = ServiceLocator()
        self.assertFalse(sl.has('test'))

    def test_has_service_exists(self):
        sl = ServiceLocator()
        sl.set('simple-service', lambda: 25 )
        self.assertTrue(sl.has('simple-service'))

    def test_has_alias_exists(self):
        sl = ServiceLocator()
        sl.set('simple-service', lambda: 26 )
        sl.create_alias('s-s', 'simple-service')
        self.assertTrue(sl.has('simple-service'))

######## sl.set() tests ################

    def test_set_empty(self):
        sl = ServiceLocator()
        with self.assertRaises(NameError):
            sl.set('', lambda: "test")

    def test_set_with_values(self):
        def simple_service():
            return "text"
        sl = ServiceLocator()
        sl.set('simple-service', simple_service)
        self.assertTrue(sl.has('simple-service'))

    def test_set_double(self):
        def simple_service():
            return "text"
        def simple_service2():
            return "text"
        sl = ServiceLocator()
        with self.assertRaises(KeyError):
            sl.set('simple-service', simple_service)
            sl.set('simple-service', simple_service2)

    def test_set_alias_exist(self):
        def simple_service():
            return "text"
        def simple_service2():
            return "text"
        sl = ServiceLocator()

        sl.set('simple-service', simple_service)
        sl.create_alias('s-s', 'simple-service')

        with self.assertRaises(KeyError):
            sl.set('s-s', simple_service2)

    def test_set_double_override(self):
        def simple_service():
            return "text"
        def simple_service2():
            return "text2"
        sl = ServiceLocator()

        sl.set('simple-service', simple_service)
        #shouldn't generate any error
        sl.set('simple-service', simple_service2, can_override=True)
        #simple-service should point to simple_service2 now
        self.assertEqual(sl.get('simple-service'), 'text2')

    def test_set_non_callable(self):
        sl = ServiceLocator()
        o = 123
        with self.assertRaises(ValueError):
            sl.set('wrong-service', o)

######## sl.get() tests ################

    def test_get_not_exists(self):
        sl = ServiceLocator()
        with self.assertRaises(KeyError):
            sl.get('non-exists-service')

    def test_get_exists(self):
        def serv():
            return "1-2-3"
        sl = ServiceLocator()
        sl.set('test-service', serv)
        val = sl.get('test-service')
        self.assertEqual(val, '1-2-3')

    def test_get_alias_exists(self):
        def serv():
            return "1-2-3"
        sl = ServiceLocator()
        sl.set('test-service', serv)
        sl.create_alias('t-s', 'test-service')
        val = sl.get('t-s')
        self.assertEqual(val, '1-2-3')

    stored_value = 5
    def test_get_value_cache(self):
        def serv():
            self.stored_value = self.stored_value ** 2
            return self.stored_value
        sl = ServiceLocator()
        sl.set('test-service', serv)
        val = sl.get('test-service')
        self.assertEqual(val, 25)
        val2 = sl.get('test-service')
        self.assertEqual(val2, 25)
        val3 = sl.get('test-service')
        self.assertEqual(val3, 25)


######### sl.create_alias() tests ############

    def test_create_empty_alias(self):
        sl = ServiceLocator()
        with self.assertRaises(NameError):
            sl.create_alias('', '')

    def test_create_alias_service_non_exists(self):
        sl = ServiceLocator()
        with self.assertRaises(KeyError):
            sl.create_alias('test', 'non-exists-service')

    def test_create_alias_name_reserved(self):
        sl = ServiceLocator()
        sl.set('serv', lambda: 'test')
        sl.create_alias('test', 'serv')

        with self.assertRaises(KeyError):
            sl.create_alias('test', 'serv')
        with self.assertRaises(KeyError):
            sl.create_alias('serv', 'test')

    def test_create_alias(self):
        sl = ServiceLocator()
        sl.set('service-1', lambda: "test-value")
        sl.create_alias('test', 'service-1')
        self.assertEqual(sl.get('test'),'test-value')

    def test_multiple_aliases_stack(self):
        sl = ServiceLocator()
        sl.set('service-1', lambda: "test-value")
        sl.create_alias('test', 'service-1')
        sl.create_alias('test2', 'test')
        sl.create_alias('checking', 'test2')
        sl.create_alias('para-pam', 'checking')
        sl.create_alias('pom-pom', 'test2')

        self.assertEqual(sl.get('test'),'test-value')
        self.assertEqual(sl.get('test2'),'test-value')
        self.assertEqual(sl.get('checking'),'test-value')
        self.assertEqual(sl.get('para-pam'),'test-value')
        self.assertEqual(sl.get('pom-pom'),'test-value')
        self.assertEqual(sl.get('service-1'),'test-value')