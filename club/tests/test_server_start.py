from django.test import LiveServerTestCase
from django.urls import reverse
import requests
import time


class ServerStartTestCase(LiveServerTestCase):
    def test_server_start(self):
        # Try starting the server
        self.assertIsNotNone(self.live_server_url)

        # Wait for the server to start (adjust sleep time as needed)
        time.sleep(2)

        # Attempt to send a request to the server
        try:
            # Replace 'index' with your URL name or path
            response = requests.get(
                self.live_server_url)
            # Check if the response status is OK
            self.assertEqual(response.status_code, 200)
        except requests.RequestException as e:
            self.fail(f"Failed to start server: {e}")
