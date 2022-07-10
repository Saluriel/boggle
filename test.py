from unittest import TestCase
from app import app
from flask import session
from boggle import Boggle


class FlaskTests(TestCase):

    def setUp(self):
        """Runs before every test"""

        self.client = app.test_client()
        app.config['TESTING'] = True

    def test_homepage(self):
        """Make sure the homepage is displaying correctly"""

        with self.client:
            res = self.client.get('/')
            self.assertIn('board', session)
            self.assertIsNone(session.get('highscore'))
            self.assertIn(b'Score:', res.data)

    def test_word_submit(self):
        """Test when submitting a word if it is correct"""

        with self.client as client:
            with client.session_transaction as session:
                session['board'] = [["T", "E", "S", "T", "T"], 
                                 ["T", "E", "S", "T", "T"],
                                 ["T", "E", "S", "T", "T"],
                                 ["T", "E", "S", "T", "T"],
                                 ["T", "E", "S", "T", "T"]]

        res = self.client.get('/check-word?word=test')
        self.assertEqual(res.json['result'], 'ok')

    def test_invalid_word(self):
        """Test if the word is in the dictionary"""

        self.client.get('/')
        res = self.client.get('/check-word?word=thisisntaword')
        self.assertEqual(res.json['result'], 'not-word')

    def test_not_on_board(self):
        """Test for when the word isn't on the board"""

        self.client.get('/')
        res = self.client.get('/check-word?word=abarticulation')
        self.assertEqual(res.json['result'], 'not-on-board')