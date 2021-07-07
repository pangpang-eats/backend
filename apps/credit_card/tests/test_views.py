import typing
from rest_framework.test import APITestCase
from apps.user.models import User, UserRole
from apps.credit_card.models import CreditCard


def create_sample_user_and_get_token(api_client, phone_number) -> typing.List:
    user: User = User.objects.create_user(phone_number=phone_number,
                                          name='홍길동',
                                          password='thePas123Q',
                                          role=UserRole.CLIENT)
    response = api_client.post(
        '/api/token',
        {
            'phone_number': phone_number,
            'password': 'thePas123Q',
        },
    )
    return (user, response.data['access'])


class TestCreditCardAssignmentView(APITestCase):
    ENDPOINT = '/api/credit-card'
    access_token: str
    """
    Test the API to assign a credit card

    the credit card should be only assigned when:
    1. user is authenticated
    2. the card number and cvc fields should be filled
    3. the card number's length should be 16 (the visa card)
    4. the cvc should be 3 digits
    5. the expiry_month should be between 1 and 12
    6. the expiry_year should be bigger than the current year
    """
    def setUp(self):
        self.client = self.APIClient()
        _, self.access_token = create_sample_user_and_get_token(
            self.client, '01012341234')

    def test_assignment_should_success(self):
        """
        this function tests the credit card assignment process,
        1. create a sample user (like I've done in TestUserRegistration.test_user_registration_should_success)
        2. issue a jwt token, by send post request to '/api/token' with the sample user's phone_number and password
        3. using the obtained jwt token, embed it into header, like <authorization: Bearer <jwt_token>>
        4. send post request to '/api/users/creditcard'
        5. check it's response.status_code is 201
        """
        response = self.client.post(
            self.ENDPOINT,
            {
                'owner_first_name': '길동',
                'owner_last_name': '홍',
                'alias': '홍길동의 카드',
                'card_number': '4111111111111111',
                'cvc': '123',
                'expiry_year': 2024,
                'expiry_month': 12,
            },
            HTTP_AUTHORIZATION='Bearer ' + self.access_token,
        )
        self.assertEqual(response.status_code, 201)

    def test_assignment_with_wrong_card_number_should_fail(self):
        """
        other conditions are the same as the 'test_credit_card_assignment_should_success'
        but the card number should be '1234' and it should be failed, and you have to assert that is failed
        """
        self.client = self.APIClient()
        response = self.client.post(
            self.ENDPOINT,
            {
                'owner_first_name': '길동',
                'owner_last_name': '홍',
                'alias': '홍길동의 카드',
                'card_number': '1234',
                'cvc': '123',
                'expiry_year': 2024,
                'expiry_month': 12,
            },
            HTTP_AUTHORIZATION='Bearer ' + self.access_token,
        )
        self.assertEqual(response.status_code, 400)

    def test_without_token_should_fail(self):
        """
        send post request to assign a credit card like I've done from the two upper functions,
        but without the credentials
        """
        self.client = self.APIClient()
        response = self.client.post(
            self.ENDPOINT,
            {
                'owner_first_name': '길동',
                'owner_last_name': '홍',
                'alias': '홍길동의 카드',
                'card_number': '4111111111111111',
                'cvc': '123',
                'expiry_year': 2024,
                'expiry_month': 12,
            },
        )
        self.assertEqual(response.status_code, 401)

    def test_with_wrong_expiry_year_should_fail(self):
        """
        send post request to assign a credit card with credentials,
        but the parameter 'expiry_year' should be 1990 (which is expired a long time ago)
        """
        self.client = self.APIClient()
        response = self.client.post(
            self.ENDPOINT,
            {
                'owner_first_name': '길동',
                'owner_last_name': '홍',
                'alias': '홍길동의 카드',
                'card_number': '4111111111111111',
                'cvc': '123',
                'expiry_year': 1990,
                'expiry_month': 12,
            },
            HTTP_AUTHORIZATION='Bearer ' + self.access_token,
        )
        self.assertEqual(response.status_code, 400)

    def test_with_wrong_expiry_month_should_fail_1(self):
        """
        assign credit card with wrong expiry_month, like 13
        """
        self.client = self.APIClient()
        response = self.client.post(
            self.ENDPOINT,
            {
                'owner_first_name': '길동',
                'owner_last_name': '홍',
                'alias': '홍길동의 카드',
                'card_number': '4111111111111111',
                'cvc': '123',
                'expiry_year': 2024,
                'expiry_month': 13,
            },
            HTTP_AUTHORIZATION='Bearer ' + self.access_token,
        )
        self.assertEqual(response.status_code, 400)

    def test_with_wrong_expiry_month_should_fail_2(self):
        """
        assign credit card with wrong expiry_month, like -1
        """
        self.client = self.APIClient()
        response = self.client.post(
            self.ENDPOINT,
            {
                'owner_first_name': '길동',
                'owner_last_name': '홍',
                'alias': '홍길동의 카드',
                'card_number': '4111111111111111',
                'cvc': '123',
                'expiry_year': 2024,
                'expiry_month': -1,
            },
            HTTP_AUTHORIZATION='Bearer ' + self.access_token,
        )
        self.assertEqual(response.status_code, 400)

    def test_with_wrong_cvc_should_fail(self):
        """
        assign a credit card, but the value of 'cvc' should be abc
        """
        self.client = self.APIClient()
        response = self.client.post(
            self.ENDPOINT,
            {
                'owner_first_name': '길동',
                'owner_last_name': '홍',
                'alias': '홍길동의 카드',
                'card_number': '4111111111111111',
                'cvc': 'abc',
                'expiry_year': 2024,
                'expiry_month': 12,
            },
            HTTP_AUTHORIZATION='Bearer ' + self.access_token,
        )
        self.assertEqual(response.status_code, 400)
        """
        1. delete an existing card
        2. assert that the card is deleted
        """
        self.client = self.APIClient()
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' +
                                self.user1_token)
        response = self.client.delete(self.ENDPOINT + '/1')
        self.assertEqual(response.status_code, 204)