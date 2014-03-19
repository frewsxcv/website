from c101ws.web import insecureSite, _withHSTS
from twisted.trial.unittest import SynchronousTestCase
from twisted.web.server import Request
from twisted.web.util import Redirect


class FakeRequest(object):
    def __init__(self, path):
        self.path = path
        self.prepath = []
        self.postpath = path.split("/")



class HSTSTests(object):
    def test_withHSTS(self):
        requestFactoryWithHSTS = _withHSTS(Request)
        responseHeaders = requestFactoryWithHSTS().responseHeaders
        value, = responseHeaders.getRawHeaders("Strict-Transport-Security")
        self.assertEqual(value, "max-age=31536000")



class InsecureSiteTests(SynchronousTestCase):
    def setUp(self):
        self.site = insecureSite()


    def test_redirectsToSecureSite(self):
        """Requests made to the site redirect to the secure site.

        """
        self.assertRedirectsToSecureSite("/")
        self.assertRedirectsToSecureSite("/a/b/c")


    def assertRedirectsToSecureSite(self, path):
        """Asserts that a request to this path would have resulted in a
        redirect to the secure website.

        """
        request = FakeRequest(path)
        resource = self.site.getResourceFor(request)
        self.assertTrue(isinstance(resource, Redirect))
        self.assertEqual(resource.url, "https://www.crypto101.io")
