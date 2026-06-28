import unittest
import json
import os

# Set environment to force mock fallback database during tests
os.environ['FIREBASE_CREDENTIALS_PATH'] = 'non_existent_file_to_force_mock.json'

from app import app, NEWS_ARTICLES, PLAYERS, SHOP_ITEMS

class QuinsAppTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True
        
        # Clear mock data files before each test to maintain state independence
        for name in ['public_comments', 'newsletter_subscribers']:
            file_path = f"mock_{name}.json"
            if os.path.exists(file_path):
                try:
                    os.remove(file_path)
                except Exception:
                    pass

    def tearDown(self):
        # Clean up mock files after testing
        for name in ['public_comments', 'newsletter_subscribers']:
            file_path = f"mock_{name}.json"
            if os.path.exists(file_path):
                try:
                    os.remove(file_path)
                except Exception:
                    pass

    def test_pages_load(self):
        """Verify that all user-facing pages load successfully (200 OK)."""
        routes = ['/', '/news', '/players', '/fixtures', '/shop', '/tickets', '/about']
        for route in routes:
            response = self.app.get(route)
            self.assertEqual(response.status_code, 200, f"Route {route} failed to load.")
            self.assertIn(b'Quins', response.data, f"Brand 'Quins' missing on route {route}.")

    def test_news_search(self):
        """Verify search query filtering on news page."""
        response = self.app.get('/news?q=Christie')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Christie', response.data)

    def test_comment_submission(self):
        """Verify posting comments works and inputs are saved."""
        # Test posting empty comment (fails)
        response = self.app.post('/api/comment', data={'username': 'Test User', 'text': ''})
        self.assertEqual(response.status_code, 400)
        
        # Test posting valid comment (succeeds)
        response = self.app.post('/api/comment', data={'username': 'Rugby Fan', 'text': 'Go Quins!'})
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertTrue(data['success'])
        
        # Verify comment is listed
        response = self.app.get('/api/comments')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertTrue(data['success'])
        self.assertEqual(len(data['comments']), 1)
        self.assertEqual(data['comments'][0]['username'], 'Rugby Fan')
        self.assertEqual(data['comments'][0]['text'], 'Go Quins!')

    def test_newsletter_subscription(self):
        """Verify newsletter subscription and validations."""
        # Missing fields (fails)
        response = self.app.post('/api/subscribe', data={'name': 'Jane', 'email': 'jane@example.com'})
        self.assertEqual(response.status_code, 400)
        
        # Missing consent (fails)
        response = self.app.post('/api/subscribe', data={'name': 'Jane', 'surname': 'Smith', 'email': 'jane@example.com'})
        self.assertEqual(response.status_code, 400)
        
        # Successful subscription (succeeds)
        response = self.app.post('/api/subscribe', data={
            'name': 'Jane',
            'surname': 'Smith',
            'email': 'jane@example.com',
            'consent': 'on'
        })
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertTrue(data['success'])

if __name__ == '__main__':
    unittest.main()
