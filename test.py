from unittest import TestCase
from app import app
from flask import session
from boggle import Boggle


class FlaskTests(TestCase):

    def setUp(self):
        """Stuff to do before every test."""

        # set up the test client
        self.client = app.test_client()
        # set up the TESTING configuration variable
        app.config['TESTING'] = True

    def test_homepage(self):
        """Make sure information is in the session and HTML is displayed"""

        # use the client to make a GET request to the homepage
        with self.client:
            response = self.client.get('/')
            #  check if the 'board' key is in the session
            self.assertIn('board', session)
            # check if the 'highscore' key is not in the session
            self.assertIsNone(session.get('highscore'))
            # check if the 'nplays' key is not in the session
            self.assertIsNone(session.get('nplays'))
            # check if the HTML contains the string '<p>High Score:'
            self.assertIn(b'<p>High Score:', response.data)
            # checks if Html has the string score
            self.assertIn(b'Score:', response.data)
            # check the HTML contains the string 
            self.assertIn(b'Seconds Left:', response.data)

    def test_valid_word(self):
        """Test if word is valid by modifying the board in the session"""
        
        # check if the HTML contains the string '<p>High Score:'
        with self.client as client:
            # modify the 'board' key in the session
            with client.session_transaction() as sess:
                sess['board'] = [["D", "O", "G", "G", "G"], 
                                 ["D", "O", "G", "G", "G"], 
                                 ["D", "O", "G", "G", "G"], 
                                 ["D", "O", "G", "G", "G"], 
                                 ["D", "O", "G", "G", "G"]]
        # make a GET request to the 'check-word' endpoint with the word 'dog'
        response = self.client.get('/check-word?word=dog')
        # check if the JSON response has the 'result' key set to 'ok'
        self.assertEqual(response.json['result'], 'ok')

    def test_invalid_word(self):
        """Test if word is in the dictionary"""
        
        # use the test client to make a GET request to the homepage
        self.client.get('/')
        # make a GET request to the 'check-word' endpoint with the word 'impossible'
        response = self.client.get('/check-word?word=impossible')
        # check if the JSON response has the 'result' key set to 'not-on-board'
        self.assertEqual(response.json['result'], 'not-on-board')

    def non_english_word(self):
        """Test if word is on the board"""

        # use the test client to make a GET request to the homepage
        self.client.get('/')
        # make a GET request to the 'check-word' endpoint with a non-English word
        response = self.client.get(
            '/check-word?word=fsjdakfkldsfjdslkfjdlksf')
         # check if the JSON response has the 'result' key set to 'not-word'
        self.assertEqual(response.json['result'], 'not-word')