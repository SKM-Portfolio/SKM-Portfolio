import unittest
import json
from unittest.mock import patch, MagicMock
import sys
import os

# Add the project root to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import app
from werkzeug.security import generate_password_hash

class AppTestCase(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    @patch('app.get_db_connection')
    def test_register_success(self, mock_get_db_connection):
        mock_db = MagicMock()
        mock_cursor = MagicMock()
        mock_get_db_connection.return_value = mock_db
        mock_db.cursor.return_value = mock_cursor

        response = self.app.post('/register',
                                 data=json.dumps({'username': 'testuser', 'password': 'password', 'email': 'test@example.com'}),
                                 content_type='application/json')

        self.assertEqual(response.status_code, 201)
        self.assertIn(b'User registered successfully', response.data)

        # Check that the password was hashed
        args, kwargs = mock_cursor.execute.call_args
        self.assertIn('password_hash', args[0])
        self.assertTrue(args[1][1].startswith('scrypt:'))

    @patch('app.get_db_connection')
    def test_login_success(self, mock_get_db_connection):
        mock_db = MagicMock()
        mock_cursor = MagicMock()
        mock_get_db_connection.return_value = mock_db
        mock_db.cursor.return_value = mock_cursor

        hashed_password = generate_password_hash('password')
        mock_cursor.fetchone.return_value = {'user_id': 1, 'username': 'testuser', 'password_hash': hashed_password}

        response = self.app.post('/login',
                                 data=json.dumps({'username': 'testuser', 'password': 'password'}),
                                 content_type='application/json')

        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Login successful', response.data)

        # Ensure password hash is not in the response
        response_data = json.loads(response.data)
        self.assertNotIn('password_hash', response_data.get('user', {}))

    @patch('app.get_db_connection')
    def test_get_movies(self, mock_get_db_connection):
        mock_db = MagicMock()
        mock_cursor = MagicMock()
        mock_get_db_connection.return_value = mock_db
        mock_db.cursor.return_value = mock_cursor
        mock_cursor.fetchall.return_value = [{'movie_id': 1, 'title': 'Test Movie'}]

        response = self.app.get('/movies')

        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Test Movie', response.data)

    @patch('app.get_db_connection')
    def test_get_shows(self, mock_get_db_connection):
        mock_db = MagicMock()
        mock_cursor = MagicMock()
        mock_get_db_connection.return_value = mock_db
        mock_db.cursor.return_value = mock_cursor
        mock_cursor.fetchall.return_value = [{'show_id': 1, 'title': 'Test Movie', 'theater_name': 'Test Theater'}]

        response = self.app.get('/shows?movie_id=1')

        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Test Movie', response.data)

    @patch('app.get_db_connection')
    def test_book_ticket_success(self, mock_get_db_connection):
        mock_db = MagicMock()
        mock_cursor = MagicMock()
        mock_get_db_connection.return_value = mock_db
        mock_db.cursor.return_value = mock_cursor
        mock_cursor.fetchone.return_value = {'ticket_price': 10.00}

        response = self.app.post('/book',
                                 data=json.dumps({'user_id': 1, 'show_id': 1, 'num_tickets': 2}),
                                 content_type='application/json')

        self.assertEqual(response.status_code, 201)
        self.assertIn(b'Booking successful', response.data)

if __name__ == '__main__':
    unittest.main()
