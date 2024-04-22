import unittest
import requests

class TestInternetConnectivity(unittest.TestCase):
    def test_google_ping(self):
        """Test if Google is reachable, indicating internet connectivity."""
        response = requests.get('http://www.google.com')
        self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    unittest.main()