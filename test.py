from unittest import TestCase
from app import app
from flask import session
from boggle import Boggle

app.config['TESTING'] = True
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']

class FlaskTests(TestCase):
    @classmethod
    def setUpClass(cls):
        boggle = Boggle()
        boggle_board = boggle.make_board()

    def test_home_page(self):
        with app.test_client() as client:
            res = client.get('/')
            html = res.get_data(as_text=True)

            self.assertEqual(res.status_code, 200)

            self.assertIn('<div class="display-1 mb-4">Boggle!</div>', html)

    def test_submit_guess(self):
        with app.test_client() as client:
            res = client.get('/check-word', data={'guess': 'if'})
            html = res.get_data(as_text=True)

            self.assertEqual(res.status_code, 200)

            self.assertIn('<div class="display-1 mb-4">Boggle!</div>', html)
            self.assertIn('<div class="alert', html)