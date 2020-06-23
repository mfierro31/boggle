from unittest import TestCase
from app import app
from flask import session
from boggle import Boggle

app.config['TESTING'] = True
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']

class FlaskTests(TestCase):
    def test_home_page(self):
        with app.test_client() as client:
            res = client.get('/')

            html = res.get_data(as_text=True)

            self.assertEqual(res.status_code, 200)

            self.assertIn('border border-dark">', html)

            self.assertIn('board', session)
            self.assertIn('times_visited', session)
            self.assertIn('scores', session)
            self.assertIn('guess', session)


    def test_valid_word(self):
        with app.test_client() as client:
            with client.session_transaction() as sess:
                sess['board'] = [["C", "A", "T", "T", "T"], 
                                 ["C", "A", "T", "T", "T"], 
                                 ["C", "A", "T", "T", "T"], 
                                 ["C", "A", "T", "T", "T"], 
                                 ["C", "A", "T", "T", "T"]]

                sess['guess'] = ['dog']

        response = client.get('/check-word?guess=cat')
        self.assertEqual(response.json['result'], 'ok')

    def test_not_on_board(self):
        with app.test_client() as client:
            client.get('/')
            res = client.get('/check-word?guess=impossible')
            self.assertEqual(res.json['result'], 'not-on-board')

    def test_not_a_word(self):
        with app.test_client() as client:
            client.get('/')
            res = client.get('/check-word?guess=crflm')
            self.assertEqual(res.json['result'], 'not-a-word')

    def test_already_used(self):
        with app.test_client() as client:
            client.get('/')

            with client.session_transaction() as sess:
                sess['guess'] = ['dog']

        res = client.get('/check-word?guess=dog')
        self.assertEqual(res.json['result'], 'word-already-used')

