from django.test import TestCase
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from .models import books
from rest_framework.test import APITestCase
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from .models import books


# test_model.py
class BooksModelTest(TestCase):
    def setUp(self):
        self.book = books.objects.create(
            title="Python",
            author="JACK",
            description="This is a sample book.",
            published_date="2024-01-01T00:00:00Z",
            price=20.99
        )

    def test_book_creation(self):
        self.assertEqual(self.book.title, "Python")
        self.assertEqual(self.book.author, "JACK")
        self.assertEqual(self.book.description, "This is a sample book.")
        self.assertEqual(str(self.book.price), '20.99')

    def test_title_validation(self):
        with self.assertRaises(ValidationError):
            book = books(title='', author='Jane Doe', price=10.00)
            #  raise a ValidationError
            book.clean()       
            from django.contrib.auth.models import User

#API_View_TestCase

class AuthTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password')
        self.login_url = '/api/login/'  
        self.signup_url = '/api/signup/'
        self.token = self.get_jwt_token(self.user)

    def get_jwt_token(self, user):
        refresh = RefreshToken.for_user(user)
        return {
            'access': str(refresh.access_token),
            'refresh': str(refresh)
        }

    def test_signup(self):
        data = {'username': 'newuser', 'password': 'newpassword'}
        response = self.client.post(self.signup_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)

    def test_login(self):
        data = {'username': 'testuser', 'password': 'password'}
        response = self.client.post(self.login_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)
        
        

