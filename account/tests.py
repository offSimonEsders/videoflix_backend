from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient

from account.models import VideoflixUser
from rest_framework.authtoken.models import Token

import json


# Create your tests here.
class AccountTestCase(TestCase):
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
        self.assertEqual(response.status_code, 201)
        user = VideoflixUser.objects.all()
        return str(user[0].verification_code)

    def user_checkverifytoken(self, verification_code):
        url = reverse('checkverifytoken')
        response = self.client.post(url, {'token': verification_code}, format='json')
        self.assertEqual(response.status_code, 200)

    def verify_user(self, verification_code):
        url = reverse('verifyuser')
        response = self.client.post(url, {'token': verification_code}, format='json')
        self.assertEqual(response.status_code, 200)

    def login_user(self, register = True):
        if register:
            verification_code = self.register_user()
            self.user_checkverifytoken(verification_code)
            self.verify_user(verification_code)
        url = reverse('login')
        response = self.client.post(url, {'email': self.data['email'], 'password': self.data['password']},
                                    format='json')
        user = VideoflixUser.objects.get(email=self.data['email'])
        self.client.force_authenticate(user=user, token=response.data)
        return response.data

    def checkresetcode(self):
        user = VideoflixUser.objects.get(email=self.data['email'])
        url = reverse('checkresetcode')
        response = self.client.post(url, {'token': user.reset_code}, format='json')
        self.assertEqual(response.status_code, 200)

    def changepassword(self):
        user = VideoflixUser.objects.get(email=self.data['email'])
        url = reverse('changepassword')
        response = self.client.post(url, {'token': user.reset_code, 'password': 'ABCDEFG13'}, format='json')
        self.data.update({'password': 'ABCDEFG13'})
        self.login_user(False)
        self.assertEqual(response.status_code, 200)

    def test_register_user(self):
        self.register_user()

    def test_user_checkverifytoken(self):
        verification_code = self.register_user()
        self.user_checkverifytoken(verification_code)

    def test_user_verification(self):
        verification_code = self.register_user()
        self.verify_user(verification_code)

    def test_login_user(self):
        self.login_user()

    def test_logout_user(self):
        auth_token = self.login_user()
        url = reverse('logout')
        response = self.client.delete(url, {'token': auth_token['response']}, format='json')
        self.assertEqual(response.status_code, 200)

    def test_requestresetpassword(self):
        self.login_user()
        url = reverse('requestresetpassword')
        response = self.client.post(url, {'email': self.data['email']}, format='json')
        self.checkresetcode()
        self.changepassword()
        self.assertEqual(response.status_code, 200)
