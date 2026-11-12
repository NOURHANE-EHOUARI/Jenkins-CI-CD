import unittest
from app import app


class TestAppExtra(unittest.TestCase):
    """Additional tests run in parallel with test_app.py in the Jenkins pipeline."""

    def setUp(self):
        self.client = app.test_client()
        self.client.testing = True

    def test_home_contains_calculator(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Simple Calculator', response.data)

    def test_hello_with_spaces_only(self):
        # A name made of spaces is stripped, so the default greeting is shown
        response = self.client.post('/hello', data={'username': '   '})
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Hello there', response.data)

    def test_sum_negative_numbers(self):
        response = self.client.post('/sum', data={'a': '-2', 'b': '5'})
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'3.0', response.data)

    def test_sum_decimal_numbers(self):
        response = self.client.post('/sum', data={'a': '1.5', 'b': '2.25'})
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'3.75', response.data)

    def test_sum_missing_value_defaults_to_zero(self):
        response = self.client.post('/sum', data={'a': '4'})
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'4.0', response.data)

    def test_hello_get_not_allowed(self):
        response = self.client.get('/hello')
        self.assertEqual(response.status_code, 405)

    def test_unknown_route_returns_404(self):
        response = self.client.get('/does-not-exist')
        self.assertEqual(response.status_code, 404)


if __name__ == "__main__":
    unittest.main()
