from rest_framework.test import APITestCase
from apps.common.test import create_sample_user_and_get_token
from apps.user.models import User
from apps.credit_card.models import CreditCard


class TestCreditCardAssignmentView(APITestCase):
    ENDPOINT = '/api/credit-cards'
    access_token: str
    """
    Test the API to assign a credit card

    the credit card should only be assigned when:
    1. the user is authenticated
    2. the card number and cvc fields should be filled
    3. the card number's length should be 16 (the visa card)
    4. the cvc should be 3 digits
    5. the expiry_month should be between 1 and 12
    6. the expiry_year should be bigger than the current year
    """
    def setUp(self):
        _, self.access_token = create_sample_user_and_get_token(
            self.client, '01012341234')

    def test_assignment_should_success(self):
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


class TestCreditCardView(APITestCase):
    ENDPOINT = '/api/credit-cards'
    user1: User
    user2: User
    user1_token: str
    user2_token: str
    """
    Test the API self.ENDPOINT to features for credit card

    the self.ENDPOINT should work like:
    1. it should return 401 when accessing to a specific card (like get, delete)
       without credentials or if the requested user is not the owner
    2. three api self.ENDPOINTs should work in total with credentials, and they are:
        2-1. list view
        2-2. detail view (get) - 404 if the there are no card with the given pk
        2-3. update and partial_update view (put, patch) - 404 if there are no card with the given pk
        2-3.1. but the 'alias' field only can be editted
        2-4. delete view - 404 if there are no card with the given pk
    """
