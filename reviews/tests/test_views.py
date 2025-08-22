from django.test import TestCase, Client
from django.urls import reverse


class PagesTestCase(TestCase):
	def setUp(self):
		self.client = Client()

	def test_home(self):
		resp = self.client.get(reverse('home'))
		self.assertEqual(resp.status_code, 200)

	def test_analyze_get(self):
		resp = self.client.get(reverse('review_input'))
		self.assertEqual(resp.status_code, 200)

	def test_dashboard_empty(self):
		resp = self.client.get(reverse('dashboard'))
		self.assertEqual(resp.status_code, 200)

	def test_api_stats(self):
		resp = self.client.get(reverse('api_stats'))
		self.assertEqual(resp.status_code, 200)
		self.assertIn('application/json', resp['Content-Type'])



