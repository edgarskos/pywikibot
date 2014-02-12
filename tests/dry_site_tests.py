import pywikibot
from pywikibot.site import must_be

from utils import PywikibotTestCase, unittest


class DrySite(pywikibot.site.APISite):
    @property
    def userinfo(self):
        return self._userinfo


class TestDrySite(PywikibotTestCase):
    def test_logged_in(self):
        x = DrySite('en')

        x._userinfo = {'name': None, 'groups': []}
        x._username = ['normal_user', 'sysop_user']

        self.assertFalse(x.logged_in(True))
        self.assertFalse(x.logged_in(False))

        x._userinfo['name'] = 'normal_user'
        self.assertFalse(x.logged_in(True))
        self.assertTrue(x.logged_in(False))

        x._userinfo['name'] = 'sysop_user'
        x._userinfo['groups'] = ['sysop']
        self.assertTrue(x.logged_in(True))
        self.assertFalse(x.logged_in(False))


class TestMustBe(PywikibotTestCase):
    """Test cases for the must_be decorator."""

    # Implemented without setUpClass(cls) and global variables as objects
    # were not completely disposed and recreated but retained 'memory'
    def setUp(self):
        self.code = 'test'
        self.family = lambda: None
        self.family.name = 'test'
        self._logged_in_as = None
        self.obsolete = False

    def login(self, sysop):
        # mock call
        self._logged_in_as = 'sysop' if sysop else 'user'

    def testMockInTest(self):
        self.assertEqual(self._logged_in_as, None)
        self.login(True)
        self.assertEqual(self._logged_in_as, 'sysop')

    testMockInTestReset = testMockInTest

    @must_be('sysop')
    def call_this_sysop_req_function(self, *args, **kwargs):
        return args, kwargs

    @must_be('user')
    def call_this_user_req_function(self, *args, **kwargs):
        return args, kwargs

    def testMustBeSysop(self):
        args = (1, 2, 'a', 'b')
        kwargs = {'i': 'j', 'k': 'l'}
        retval = self.call_this_sysop_req_function(*args, **kwargs)
        self.assertEqual(retval[0], args)
        self.assertEqual(retval[1], kwargs)
        self.assertEqual(self._logged_in_as, 'sysop')

    def testMustBeUser(self):
        args = (1, 2, 'a', 'b')
        kwargs = {'i': 'j', 'k': 'l'}
        retval = self.call_this_user_req_function(*args, **kwargs)
        self.assertEqual(retval[0], args)
        self.assertEqual(retval[1], kwargs)
        self.assertEqual(self._logged_in_as, 'user')

    def testOverrideUserType(self):
        args = (1, 2, 'a', 'b')
        kwargs = {'i': 'j', 'k': 'l'}
        retval = self.call_this_user_req_function(*args, as_group='sysop', **kwargs)
        self.assertEqual(retval[0], args)
        self.assertEqual(retval[1], kwargs)
        self.assertEqual(self._logged_in_as, 'sysop')

    def testObsoleteSite(self):
        self.obsolete = True
        args = (1, 2, 'a', 'b')
        kwargs = {'i': 'j', 'k': 'l'}
        self.assertRaises(pywikibot.NoSuchSite, self.call_this_user_req_function, args, kwargs)

if __name__ == '__main__':
    unittest.main()
