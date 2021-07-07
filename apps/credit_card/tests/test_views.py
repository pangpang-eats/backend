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


class TestCreditCardView(APITestCase):
    ENDPOINT = '/api/credit-card'
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
    def setUp(self):
        # issue a token
        self.client = self.APIClient()
        self.user1, self.user1_token = create_sample_user_and_get_token(
            self.client, '01012341234')
        self.user2, self.user2_token = create_sample_user_and_get_token(
            self.client, '01000000000')
        # create cards for each of the users
        ## create two cards for user 1
        CreditCard.objects.create(
            owner=self.user1,
            owner_first_name='길동',
            owner_last_name='홍',
            alias='홍길동의 카드1',
            card_number='4111111111111111',
            cvc='123',
            expiry_year=2024,
            expiry_month=12,
        )
        CreditCard.objects.create(
            owner=self.user1,
            owner_first_name='길동',
            owner_last_name='홍',
            alias='홍길동의 카드2',
            card_number='1234567890123456',
            cvc='123',
            expiry_year=2024,
            expiry_month=12,
        )
        ## create three cards for user 2
        CreditCard.objects.create(
            owner=self.user2,
            owner_first_name='길동',
            owner_last_name='홍',
            alias='길동 홍씨의 카드1',
            card_number='0123456789012345',
            cvc='123',
            expiry_year=2024,
            expiry_month=12,
        )
        CreditCard.objects.create(
            owner=self.user2,
            owner_first_name='길동',
            owner_last_name='홍',
            alias='길동홍씨의 카드2',
            card_number='2234567890123456',
            cvc='123',
            expiry_year=2024,
            expiry_month=12,
        )
        CreditCard.objects.create(
            owner=self.user2,
            owner_first_name='길동',
            owner_last_name='홍',
            alias='길동홍씨의 카드3',
            card_number='1234567890123456',
            cvc='123',
            expiry_year=2024,
            expiry_month=12,
        )

    def test_list_view_should_return_401(self):
        response = self.client.get(self.ENDPOINT)
        self.assertEqual(response.status_code, 401)

    def test_list_view_should_success_1(self):
        """
        1. get the list of assigned credit card using the token of user2
        2. the length of the list should be 3
        """
        self.client = self.APIClient()
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' +
                                self.user2_token)
        response = self.client.get(self.ENDPOINT)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 3)

    def test_list_view_should_success_2(self):
        """
        1. get the list of assigned credit card using the token of user1
        2. the length of the list should be 2
        """
        self.client = self.APIClient()
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' +
                                self.user1_token)
        response = self.client.get(self.ENDPOINT)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 2)

    def test_detail_view_should_return_401(self):
        """
        1. get the detail of a card without the credentials
        2. the response status code should be 401
        """
        self.client = self.APIClient()
        response = self.client.get(self.ENDPOINT + '/1')
        self.assertEqual(response.status_code, 401)

    def test_detail_view_should_return_403(self):
        """
        1. get the detail of a card that exists, but with the wrong user
        2. the response should be 403
        """
        self.client = self.APIClient()
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' +
                                self.user2_token)
        response = self.client.get(self.ENDPOINT + '/1')
        self.assertEqual(response.status_code, 403)

    def test_detail_view_should_return_404(self):
        """
        1. get the detail of a card that does not exist
        2. the response should be 404
        """
        self.client = self.APIClient()
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' +
                                self.user2_token)
        response = self.client.get(self.ENDPOINT + '/100', )
        self.assertEqual(response.status_code, 404)

    def test_detail_view_should_success(self):
        """
        1. get the detail of a card that exists
        2. the response should be 200
        3. and all of the fields should be returned, also the value should be the same
        """
        self.client = self.APIClient()
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' +
                                self.user1_token)
        response = self.client.get(self.ENDPOINT + '/1')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['alias'], '홍길동의 카드1')
        self.assertEqual(response.data['card_number'], '4111111111111111')
        self.assertEqual(response.data['cvc'], '123')
        self.assertEqual(response.data['expiry_year'], '2024')
        self.assertEqual(response.data['expiry_month'], '12')
        self.assertEqual(response.data['owner_first_name'], '길동')
        self.assertEqual(response.data['owner_last_name'], '홍')

    def test_update_view_should_return_401(self):
        """
        1. request to update a existing card without the credentials
        2. the response status code should be 401
        """
        response = self.client.put(self.ENDPOINT + '/1',
                                   data={'alias': '카드 이름'})
        self.assertEqual(response.status_code, 401)

    def test_update_view_should_return_403(self):
        """
        1. update an existing card (the id is 1), using the user2's token
        2. the response status code should be 403
        """
        self.client = self.APIClient()
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' +
                                self.user2_token)
        response = self.client.put(self.ENDPOINT + '/1',
                                   data={'alias': '카드 이름'})
        self.assertEqual(response.status_code, 403)

    def test_update_view_should_return_404(self):
        """
        1. get the detail of a card that does not exist
        2. the response should be 404
        """
        self.client = self.APIClient()
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' +
                                self.user2_token)
        response = self.client.put(self.ENDPOINT + '/100',
                                   data={'alias': '카드 이름'})
        self.assertEqual(response.status_code, 404)

    def test_update_view_should_success(self):
        """
        1. update a card with put request
        2. trying to change the all of the fields:
            owner_first_name
            owner_last_name
            alias
            card_number
            cvc
            expiry_year
            expiry_month
        3. assert that only the 'alias' field has been changed, and other fields are still the same
        """
        self.client = self.APIClient()
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' +
                                self.user1_token)
        response = self.client.put(self.ENDPOINT + '/1',
                                   data={
                                       'owner_first_name': '길동',
                                       'owner_last_name': '홍',
                                       'alias': '카드 이름',
                                       'card_number': '4111111111111111',
                                       'cvc': '123',
                                       'expiry_year': '2024',
                                       'expiry_month': '12'
                                   })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['alias'], '카드 이름')
        self.assertEqual(response.data['card_number'], '4111111111111111')
        self.assertEqual(response.data['cvc'], '123')
        self.assertEqual(response.data['expiry_year'], '2024')
        self.assertEqual(response.data['expiry_month'], '12')
        self.assertEqual(response.data['owner_first_name'], '길동')
        self.assertEqual(response.data['owner_last_name'], '홍')

    def test_partial_update_view_should_success(self):
        """
        same as the upper function, but now the request method is patch
        """
        self.client = self.APIClient()
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' +
                                self.user1_token)
        response = self.client.patch(self.ENDPOINT + '/1',
                                     data={
                                         'owner_first_name': '길동',
                                         'owner_last_name': '홍',
                                         'alias': '카드 이름',
                                         'card_number': '4111111111111111',
                                         'cvc': '123',
                                         'expiry_year': '2024',
                                         'expiry_month': '12'
                                     })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['alias'], '카드 이름')
        self.assertEqual(response.data['card_number'], '4111111111111111')
        self.assertEqual(response.data['cvc'], '123')
        self.assertEqual(response.data['expiry_year'], '2024')
        self.assertEqual(response.data['expiry_month'], '12')
        self.assertEqual(response.data['owner_first_name'], '길동')
        self.assertEqual(response.data['owner_last_name'], '홍')

    def test_delete_view_should_return_404(self):
        """
        1. get the detail of a card that does not exist
        2. the response should be 404
        """
        self.client = self.APIClient()
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' +
                                self.user2_token)
        response = self.client.delete(self.ENDPOINT + '/100')
        self.assertEqual(response.status_code, 404)

    def test_delete_view_should_return_401(self):
        """
        1. delete an existing card without the credentials
        2. the response status code should be 401
        """
        response = self.client.delete(self.ENDPOINT + '/1')
        self.assertEqual(response.status_code, 401)

    def test_delete_view_should_return_403(self):
        """
        1. delete an existing card using wrong user
        2. the response status should be 403
        """
        self.client = self.APIClient()
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' +
                                self.user2_token)
        response = self.client.delete(self.ENDPOINT + '/1')
        self.assertEqual(response.status_code, 403)

    def test_delete_view_should_success(self):
        """
        1. delete an existing card
        2. assert that the card is deleted
        """
        self.client = self.APIClient()
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' +
                                self.user1_token)
        response = self.client.delete(self.ENDPOINT + '/1')
        self.assertEqual(response.status_code, 204)