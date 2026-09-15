from rest_framework.test import APITestCase
from users.models import User


class UserApiTests(APITestCase):
    def setUp(self):
        response = self.client.get('/api/auth/csrf/')
        self.csrf = response.json()['csrfToken']

    def test_registration_validates_and_creates_user(self):
        response = self.client.post('/api/auth/register/', {
            'username': 'User1234', 'full_name': 'Иван Иванов', 'email': 'user@example.com', 'password': 'Strong1!'
        }, format='json', HTTP_X_CSRFTOKEN=self.csrf)
        self.assertEqual(response.status_code, 201)
        self.assertTrue(User.objects.filter(username='User1234').exists())

    def test_invalid_username_rejected(self):
        response = self.client.post('/api/auth/register/', {
            'username': '1bad', 'full_name': 'Иван', 'email': 'bad@example.com', 'password': 'Strong1!'
        }, format='json', HTTP_X_CSRFTOKEN=self.csrf)
        self.assertEqual(response.status_code, 400)
