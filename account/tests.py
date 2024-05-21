from django.urls import reverse
from rest_framework.test import APIClient, APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model


class TestRegistrationAPIView(APITestCase):

    def setUp(self):
        self.client = APIClient()
        self.url = reverse('registration')
        self.data = {
            'username': 'testuser',
            'password': 'strongpassword123',
            'password2': 'strongpassword123',
            'email': 'testuser@example.com',
            'first_name': 'Test',
            'last_name': 'User',
            'phone_number': '1234567890'
        }

    def test_registration_success(self):
        response = self.client.post(self.url, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(get_user_model().objects.filter(username='testuser').exists())

        user = get_user_model().objects.get(username='testuser')
        self.assertEqual(user.email, 'testuser@example.com')
        self.assertEqual(user.first_name, 'Test')
        self.assertEqual(user.last_name, 'User')
        self.assertEqual(user.phone_number, '1234567890')
        self.assertTrue(user.check_password('strongpassword123'))

    def test_registration_password_mismatch(self):
        self.data['password2'] = 'differentpassword'
        response = self.client.post(self.url, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('password', response.data)
        self.assertEqual(response.data['password'][0], "Password fields didn't match.")
        self.assertFalse(get_user_model().objects.filter(username='testuser').exists())
