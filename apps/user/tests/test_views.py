from rest_framework.test import APITestCase


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

