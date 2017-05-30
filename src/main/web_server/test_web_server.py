from web_server import app
from web_server import mongo
import unittest


class TestWebServer(unittest.TestCase):
    data = {'date': 1111111111.0, 'text': 'test?', '_id': '11111', 'subreddit': 'test'}

    @classmethod
    def setUpClass(cls):
        pass

    @classmethod
    def tearDownClass(cls):
        pass

    def populate_db(self):
        mongo.db.save(self.data)

    def setUp(self):
        # creates a test client
        self.app = app.test_client()
        # propagate the exceptions to the test client
        self.app.testing = True

    def tearDown(self):
        pass

    def test_no_parameters(self):
        # sends HTTP GET request to the application
        # on the specified path
        result = self.app.get('/items/')

        # assert the status code of the response
        self.assertEqual(result.status_code, 400)

    def test_get_items(self):
        # sends HTTP GET request to the application
        # on the specified path
        result = self.app.get('/items/?subreddit=test&from=1111111110&to=1111111112')

        # assert the response data
        self.assertEqual(result.status_code, 200)
        self.assertEqual(result.data, "[]")

    def test_get_items_keyword(self):
        # sends HTTP GET request to the application
        # on the specified path
        result = self.app.get('/items/?subreddit=python&from=1495778337&to=1495951137&keyword=tricks')

        # assert the response data
        self.assertEqual(result.status_code, 200)


suite = unittest.TestLoader().loadTestsFromTestCase(TestWebServer)
unittest.TextTestRunner(verbosity=2).run(suite)
