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
