from rest_framework.test import APITestCase
from apps.user.models import UserRole, User


class TestUserRegistration(APITestCase):
    def test_user_registration_should_success(self):
        """
        this function tests the user registration with following processes:
        1. define client as self.APIClient
        2. send post request to '/api/users/register' using the client, with following parameters:
            phone_number = 01012341234
            name = 홍길동
            password = thePas123Q
        """
        self.client = self.APIClient()
        response = self.client.post(
            '/api/users/register',
            {
                'phone_number': '01012341234',
                'name': '홍길동',
                'password': 'thePas123Q',
            },
        )
        self.assertEqual(response.status_code, 201)

    def test_user_regstration_with_duplicated_phone_number_should_fail(self):
        """
        this function tests the user registration, whether it successfully returns 400 if the phone_number (which is unique) duplicates
        the other conditions are the same as the upper function, but trying it for twice and check whether if the last request's response.status_code is 400
        """
        self.client = self.APIClient()
        response = self.client.post(
            '/api/users/register',
            {
                'phone_number': '01012341234',
                'name': '홍길동',
                'password': 'thePas123Q',
            },
        )
        self.assertEqual(response.status_code, 201)
        response = self.client.post(
            '/api/users/register',
            {
                'phone_number': '01012341234',
                'name': '홍길동',
                'password': 'thePas123Q',
            },
        )
        self.assertEqual(response.status_code, 400)

    def test_user_registration_with_easy_password_should_fail(self):
        """
        all of the conditions are the same as the function 'test_user_registration_should_success',
        but the password should be 1234
        """
        self.client = self.APIClient()
        response = self.client.post(
            '/api/users/register',
            {
                'phone_number': '01012341234',
                'name': '홍길동',
                'password': '1234',
            },
        )
        self.assertEqual(response.status_code, 400)


class TestAuthorization(APITestCase):
    """
    this class is about the jwt authorization
    actually, the proccess of issuing token is all offered by the django-simplejwt module.
    Therefore this test only tests the authorization itself works alright (the process of checking phone_number and password is working correctly)
    """
    def setUp(self):
        """
        create a sample user
        """
        User.objects.create_user(phone_number='021231234',
                                 name='홍길동',
                                 password='thePas123Q',
                                 role=UserRole.CLIENT)

    def test_issuing_token_should_success(self):
        """
        1. get token by sending post request to '/api/token' with phone_number and password
        2. it should return 200 status code with jwt token
        """
        self.client = self.APIClient()
        response = self.client.post(
            '/api/token',
            {
                'phone_number': '01012341234',
                'password': 'thePas123Q',
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)

    def test_issuing_token_with_wrong_password_should_fail(self):
        """
        1. get token by sending post request to '/api/token' with phone_number and wrong password
        2. it should return 400 status code
        """
        self.client = self.APIClient()
        response = self.client.post(
            '/api/token',
            {
                'phone_number': '01012341234',
                'password': 'wrongPas123Q',
            },
        )
        self.assertEqual(response.status_code, 400)

    def test_issuing_token_without_info_should_fail(self):
        """
        1. get token by sending post request to '/api/token' without phone_number and password
        2. it should return 400 status code
        """
        self.client = self.APIClient()
        response = self.client.post(
            '/api/token',
            {},
        )
        self.assertEqual(response.status_code, 400)

    def test_refreshing_token_should_success(self):
        """
        1. get token by sending post request to '/api/token' with phone_number and password
        2. it should return 200 status code with jwt token
        3. send post request to '/api/token/refresh' with jwt token
        4. it should return 200 status code
        """
        self.client = self.APIClient()
        response = self.client.post(
            '/api/token',
            {
                'phone_number': '01012341234',
                'password': 'thePas123Q',
            },
        )
        self.assertEqual(response.status_code, 200)
        response = self.client.post(
            '/api/token/refresh',
            {
                'refresh': response.data['refresh'],
            },
        )
        self.assertEqual(response.status_code, 200)

    def test_verifying_token_should_success(self):
        """
        1. get token by sending post request to '/api/token' with phone_number and password
        2. it should return 200 status code with jwt token
        3. send post request to '/api/token/verify' with jwt token
        4. it should return 200 status code
        """
        self.client = self.APIClient()
        response = self.client.post(
            '/api/token',
            {
                'phone_number': '01012341234',
                'password': 'thePas123Q',
            },
        )
        self.assertEqual(response.status_code, 200)
        response = self.client.post(
            '/api/token/verify',
            {
                'token': response.data['access'],
            },
        )
        self.assertEqual(response.status_code, 200)

    def test_verifying_token_with_wrong_token_should_fail(self):
        """
        1. get token by sending post request to '/api/token' with phone_number and password
        2. it should return 200 status code with jwt token
        3. send post request to '/api/token/verify' with wrong jwt token
        4. it should return 400 status code
        """
        self.client = self.APIClient()
        response = self.client.post(
            '/api/token',
            {
                'phone_number': '01012341234',
                'password': 'thePas123Q',
            },
        )
        self.assertEqual(response.status_code, 200)
        response = self.client.post(
            '/api/token/verify',
            {
                'token': 'wrong',
            },
        )
        self.assertEqual(response.status_code, 400)
