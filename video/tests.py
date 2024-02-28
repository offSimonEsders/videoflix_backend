from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient

from account.models import VideoflixUser
from rest_framework.authtoken.models import Token

# Create your tests here.

class VideoTest(TestCase):
    data = {
        'username': 'testuser',
        'email': 'testuser@localhost.de',
        'password': '12345678'
    }
    client = ''

    def setUp(self):
        self.client = APIClient()

    def register_user(self):
        url = reverse('register')
        response = self.client.post(url, data=self.data, format='json')
        user = VideoflixUser.objects.all()
        return str(user[0].verification_code)

    def user_checkverifytoken(self, verification_code):
        url = reverse('checkverifytoken')
        response = self.client.post(url, {'token': verification_code}, format='json')

    def verify_user(self, verification_code):
        url = reverse('verifyuser')
        response = self.client.post(url, {'token': verification_code}, format='json')

    def login_user(self):
        verification_code = self.register_user()
        self.user_checkverifytoken(verification_code)
        self.verify_user(verification_code)
        url = reverse('login')
        response = self.client.post(url, {'email': self.data['email'], 'password': self.data['password']},
                                    format='json')
        user = VideoflixUser.objects.get(email=self.data['email'])
        self.client.force_authenticate(user=user, token=response.data)
        return response.data

    def test_movies(self):
        self.login_user()
        url = reverse('movies')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, 200)

    def test_series(self):
        self.login_user()
        url = reverse('series')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, 200)

    def test_moviesandseries(self):
        self.login_user()
        url = reverse('moviesandseries')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, 200)