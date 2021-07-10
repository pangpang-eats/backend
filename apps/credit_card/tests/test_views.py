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
