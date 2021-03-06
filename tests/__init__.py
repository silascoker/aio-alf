#
# encoding: utf-8

from unittest import TestCase, mock
from yarl import URL
from aiohttp import ClientResponse


class AsyncTestCase(TestCase):

    def setUp(self):
        from aiohttp.test_utils import setup_test_loop
        self.loop = setup_test_loop()
        self.loop.run_until_complete(self.setUpAsync())

    async def setUpAsync(self):
        pass

    def tearDown(self):
        from aiohttp.test_utils import teardown_test_loop
        self.loop.run_until_complete(self.tearDownAsync())
        teardown_test_loop(self.loop)

    async def tearDownAsync(self):
        pass


def make_response(loop, method, url, data=None,
                  content_type='text/plain', charset='utf-8'):
    response = ClientResponse(method, URL(url))
    response._post_init(loop, mock.Mock())

    def side_effect(*args, **kwargs):
        fut = loop.create_future()
        fut.set_result(str(data).encode(charset))
        return fut

    response.headers = {
        'Content-Type': '%s; charset=%s' % (content_type, charset)}
    content = response.content = mock.Mock()
    if data:
        content.read.side_effect = side_effect

    return response
