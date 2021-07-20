from rest_framework.test import APITestCase
from apps.common.test import create_sample_user_and_get_token
from apps.user.models import UserRole, User


class TestUserRegistration(APITestCase):
    ENDPOINT = '/api/users/register'

    def test_user_registration_should_success(self):
        response = self.client.post(
            self.ENDPOINT,
            {
                'phone_number': '01012341234',
                'name': '홍길동',
                'password': 'thePas123Q',
            },
        )
        self.assertEqual(response.status_code, 201)

    def test_user_regstration_with_duplicated_phone_number_should_fail(self):
        response = self.client.post(
            self.ENDPOINT,
            {
                'phone_number': '01012341234',
                'name': '홍길동',
                'password': 'thePas123Q',
            },
        )
        self.assertEqual(response.status_code, 201)
        response = self.client.post(
            self.ENDPOINT,
            {
                'phone_number': '01012341234',
                'name': '홍길동',
                'password': 'thePas123Q',
            },
        )
        self.assertEqual(response.status_code, 400)

    def test_user_registration_with_easy_password_should_fail(self):
        response = self.client.post(
            self.ENDPOINT,
            {
                'phone_number': '01012341234',
                'name': '홍길동',
                'password': '1234',
            },
        )
        self.assertEqual(response.status_code, 400)

    def test_user_registration_without_password_should_fail(self):
        response = self.client.post(
            self.ENDPOINT,
            {
                'phone_number': '01012341234',
                'name': '홍길동',
            },
        )
        self.assertEqual(response.status_code, 400)


class TestAuthorization(APITestCase):
    TOKEN_ENDPOINT = '/api/token'
    """
    this class is about the jwt authorization
    actually, the proccess of issuing token is all offered by the django-simplejwt module.
    Therefore this test only tests the authorization itself works alright (the process of checking phone_number and password is working correctly)
    """
    def setUp(self):
        """
        create a sample user
        """
        User.objects.create_user(phone_number='01012341234',
                                 name='홍길동',
                                 password='thePas123Q',
                                 role=UserRole.CLIENT)

    def test_issuing_token_should_success(self):
        response = self.client.post(
            self.TOKEN_ENDPOINT,
            {
                'phone_number': '01012341234',
                'password': 'thePas123Q',
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)

    def test_registered_user_issuing_should_success(self):
        response = self.client.post(
            '/api/users/register',
            {
                'phone_number': '01043211234',
                'name': '홍길동',
                'password': 'thePas123Q',
            },
        )
        self.assertEqual(response.status_code, 201)
        response = self.client.post(
            self.TOKEN_ENDPOINT,
            {
                'phone_number': '01043211234',
                'password': 'thePas123Q',
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)

    def test_issuing_token_with_wrong_password_should_fail(self):
        response = self.client.post(
            self.TOKEN_ENDPOINT,
            {
                'phone_number': '01012341234',
                'password': 'wrongPas123Q',
            },
        )
        self.assertEqual(response.status_code, 401)

    def test_issuing_token_without_info_should_fail(self):
        response = self.client.post(
            self.TOKEN_ENDPOINT,
            {},
        )
        self.assertEqual(response.status_code, 400)

    def test_refreshing_token_should_success(self):
        response = self.client.post(
            self.TOKEN_ENDPOINT,
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
        response = self.client.post(
            self.TOKEN_ENDPOINT,
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
        response = self.client.post(
            self.TOKEN_ENDPOINT,
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
        self.assertEqual(response.status_code, 401)


class TestRetrieveUserProfile(APITestCase):
    ENDPOINT = '/api/users/profile'
    token: str
    """
    Test the API endpoint to retrieve the user's profile

    the profile should work like:
    1. it should contain phone_number, name, role, is_verified and date_joined fields
    2. the password shouldn't be returned
    3. it shouldn't be returned when the user is not authenticated
    """
    def setUp(self):
        """
        create a sample user
        """
        _, self.token = create_sample_user_and_get_token(
            self.client, '01012341234')

    def test_retrieve_profile_should_success(self):
        response = self.client.get(
            self.ENDPOINT,
            HTTP_AUTHORIZATION='Bearer ' + self.token,
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn('phone_number', response.data)
        self.assertIn('name', response.data)
        self.assertIn('role', response.data)
        self.assertIn('is_verified', response.data)
        self.assertIn('date_joined', response.data)
        self.assertNotIn('password', response.data)

    def test_retrieve_profile_should_fail_when_not_authenticated(self):
        response = self.client.get(self.ENDPOINT, )
        self.assertEqual(response.status_code, 401)


class TestModifyingtUserProfile(APITestCase):
    ENDPOINT = '/api/users/profile'

    user: User
    token: str

    def setUp(self):
        """
        create a sample user
        """
        self.user, self.token = create_sample_user_and_get_token(
            self.client, '01012341234')

    def test_modifying_name_should_success(self):
        response = self.client.patch(self.ENDPOINT, {'name': '이지은'},
                                     HTTP_AUTHORIZATION="Bearer " + self.token)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['name'], "이지은")

    def test_modifying_phone_number_has_no_effect(self):
        original_phone_number = self.user.phone_number
        response = self.client.patch(self.ENDPOINT,
                                     {'phone_number': '01010101234'},
                                     HTTP_AUTHORIZATION="Bearer " + self.token)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['phone_number'], original_phone_number)


class TestSettingUserPassword(APITestCase):
    ENDPOINT = '/api/users/set_password'

    user: User
    token: str

    def setUp(self):
        """
        create a sample user
        """
        self.user, self.token = create_sample_user_and_get_token(
            self.client, '01012341234')

    def test_set_password_should_success(self):
        password = 'thetheAMZp@ss!'
        response = self.client.post(self.ENDPOINT, {'password': password},
                                    HTTP_AUTHORIZATION="Bearer " + self.token)
        self.assertEqual(response.status_code, 200)
        response = self.client.post(
            '/api/token',
            {
                'phone_number': self.user.phone_number,
                'password': password,
            },
        )
        self.assertEqual(response.status_code, 200)
