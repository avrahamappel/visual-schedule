import unittest
from pathlib import Path

from app import app


class TestWebRoutes(unittest.TestCase):
    def setUp(self) -> None:
        app.config['TESTING'] = True
        self.client = app.test_client()

    def test_home_page(self):
        res = self.client.get('/')

        strings = [b'action="/schedule" method="get"',
                   b'<input type="url" name="link">']

        for s in strings:
            self.assertTrue(s in res.data)

    def test_schedule_page_returns_422_if_no_link_provided(self):
        res = self.client.get('schedule')
        self.assertEqual('422 UNPROCESSABLE ENTITY', res.status)

    def test_schedule_page_works(self):
        res = self.client.get('schedule', query_string={'link': Path('fixtures/basic.ics').resolve().as_uri()})

        # TODO get a deterministic page render, with colors and all
        # with open('./fixtures/schedule.html') as fixture:
        #     self.assertMultiLineEqual(fixture.read(), res.get_data(as_text=True))

        self.assertTrue(b'Today\'s Schedule for "Appel Family Calendar"' in res.data)
