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
    def setUp(self):
        # issue a token
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
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' +
                                self.user2_token)
        response = self.client.get(self.ENDPOINT)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 3)

    def test_list_view_should_success_2(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' +
                                self.user1_token)
        response = self.client.get(self.ENDPOINT)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 2)

    def test_detail_view_should_return_401(self):
        credit_card_pk = CreditCard.objects.filter(owner=self.user1)[0]
        response = self.client.get(self.ENDPOINT + f'/{credit_card_pk}')
        self.assertEqual(response.status_code, 401)

    def test_detail_view_should_not_return_others_card(self):
        credit_card_pk = CreditCard.objects.filter(owner=self.user1)[0].id
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' +
                                self.user2_token)
        response = self.client.get(self.ENDPOINT + f'/{credit_card_pk}')
        self.assertEqual(response.status_code, 404)

    def test_detail_view_should_return_404(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' +
                                self.user2_token)
        response = self.client.get(self.ENDPOINT + '/1000000', )
        self.assertEqual(response.status_code, 404)

    def test_detail_view_should_success(self):
        credit_card_pk = CreditCard.objects.filter(owner=self.user1)[0].id
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' +
                                self.user1_token)
        response = self.client.get(self.ENDPOINT + f'/{credit_card_pk}')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['alias'], '홍길동의 카드1')
        self.assertEqual(response.data['card_number'], '4111111111111111')
        self.assertEqual(response.data['cvc'], '123')
        self.assertEqual(response.data['expiry_year'], 2024)
        self.assertEqual(response.data['expiry_month'], 12)
        self.assertEqual(response.data['owner_first_name'], '길동')
        self.assertEqual(response.data['owner_last_name'], '홍')

    def test_update_view_should_return_401(self):
        credit_card_pk = CreditCard.objects.filter(owner=self.user1)[0].id
        response = self.client.put(self.ENDPOINT + f'/{credit_card_pk}',
                                   data={'alias': '카드 이름'})
        self.assertEqual(response.status_code, 401)

    def test_update_view_should_return_403(self):
        credit_card_pk = CreditCard.objects.filter(owner=self.user1)[0].id
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' +
                                self.user2_token)
        response = self.client.put(self.ENDPOINT + f'/{credit_card_pk}',
                                   data={'alias': '카드 이름'})
        self.assertEqual(response.status_code, 403)

    def test_update_view_should_return_404(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' +
                                self.user2_token)
        response = self.client.put(self.ENDPOINT + '/100',
                                   data={'alias': '카드 이름'})
        self.assertEqual(response.status_code, 404)

    def test_update_view_should_success(self):
        credit_card = CreditCard.objects.filter(owner=self.user1)[0]
        alias = credit_card.alias
        card_number = credit_card.card_number
        cvc = credit_card.cvc
        expiry_year = credit_card.expiry_year
        expiry_month = credit_card.expiry_month
        owner_first_name = credit_card.owner_first_name
        owner_last_name = credit_card.owner_last_name

        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' +
                                self.user1_token)
        response = self.client.put(self.ENDPOINT + f'/{credit_card.id}',
                                   data={
                                       'owner_first_name': '길동',
                                       'owner_last_name': '홍',
                                       'alias': '카드 이름',
                                       'card_number': '4111111111111111',
                                       'cvc': '321',
                                       'expiry_year': '2025',
                                       'expiry_month': '11'
                                   })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['alias'], '카드 이름')
        self.assertEqual(response.data['card_number'], card_number)
        self.assertEqual(response.data['cvc'], cvc)
        self.assertEqual(response.data['expiry_year'], expiry_year)
        self.assertEqual(response.data['expiry_month'], expiry_month)
        self.assertEqual(response.data['owner_first_name'], owner_first_name)
        self.assertEqual(response.data['owner_last_name'], owner_last_name)

    def test_partial_update_view_should_success(self):
        credit_card_pk = CreditCard.objects.filter(owner=self.user1)[0].id
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' +
                                self.user1_token)
        response = self.client.patch(self.ENDPOINT + f'/{credit_card_pk}',
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
        self.assertEqual(response.data['expiry_year'], 2024)
        self.assertEqual(response.data['expiry_month'], 12)
        self.assertEqual(response.data['owner_first_name'], '길동')
        self.assertEqual(response.data['owner_last_name'], '홍')

    def test_delete_view_should_return_404(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' +
                                self.user2_token)
        response = self.client.delete(self.ENDPOINT + '/100')
        self.assertEqual(response.status_code, 404)

    def test_delete_view_should_return_401(self):
        response = self.client.delete(self.ENDPOINT + '/1')
        self.assertEqual(response.status_code, 401)

    def test_delete_view_should_return_403(self):
        credit_card_pk = CreditCard.objects.filter(owner=self.user1)[0].id
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' +
                                self.user2_token)
        response = self.client.delete(self.ENDPOINT + f'/{credit_card_pk}')
        self.assertEqual(response.status_code, 403)

    def test_delete_view_should_success(self):
        credit_card_pk = CreditCard.objects.filter(owner=self.user1)[0].id
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' +
                                self.user1_token)
        response = self.client.delete(self.ENDPOINT + f'/{credit_card_pk}')
        self.assertEqual(response.status_code, 204)