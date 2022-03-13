import unittest2 as unittest
from simple_webserver.app import hello

# run by `PYTHONPATH=. python3 -m pytest --junitxml results.xml simple_webserver/tests`

class TestFlaskWebServer(unittest.TestCase):
    @unittest.skip("demonstrating skipping")
    def test_skipped(self):
        self.fail("shouldn't happen")

    def test_upper(self):
        self.assertEqual('foo'.upper(), 'FOO')

    def test_hello(self):
        results = hello('Dan')
        self.assertEqual(results, 'Hello, Dan!')
