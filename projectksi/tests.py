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
            sl.set('', None)

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

    def test_set_double_override(self):
        def simple_service():
            return "text"
        def simple_service2():
            return "text2"
        sl = ServiceLocator()

        sl.set('simple-service', simple_service)
        #shouldn't generate any error
        sl.set('simple-service', simple_service2, allow_override=True)
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
        def serv(self):
            return "1-2-3"
        sl = ServiceLocator()
        sl.set('test-service', serv)
        val = sl.get('test-service')
        self.assertEqual(val, '1-2-3')

    def test_get_alias_exists(self):
        def serv(self):
            return "1-2-3"
        sl = ServiceLocator()
        sl.set('test-service', serv)
        sl.create_alias('t-s', 'test-service')
        val = sl.get('t-s')
        self.assertEqual(val, '1-2-3')

######### sl.create_alias() tests ############

    def test_create_empty_alias(self):
        sl = ServiceLocator()
        with self.assertRaises(KeyError):
            sl.create_alias('', '')

    def test_create_alias_service_non_exists(self):
        sl = ServiceLocator()
        with self.assertRaises(KeyError):
            sl.create_alias('test', 'non-exists-service')

    def test_create_alias(self):
        sl = ServiceLocator()
        sl.set('service-1', lambda: "test-value")
        sl.create_alias('test', 'service-1')
        self.assertEqual('test','test-value')