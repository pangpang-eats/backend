from django.test import TestCase
from django.db.utils import IntegrityError
from django.core.exceptions import ValidationError
from apps.user.models import UserRole, User
from apps.credit_card.models import CreditCard


class CreditCardTest(TestCase):
    def test_credit_card_creation_with_new_user_should_success(self):
        user = User.objects.create_user(phone_number='01012341234',
                                        name='홍길동',
                                        password='thePas123Q',
                                        role=UserRole.CLIENT)
        credit_card = CreditCard.objects.create(owner=user,
                                                alias='my awesome card',
                                                card_number='1234567890123456',
                                                cvc='123',
                                                expiry_year=2032,
                                                expiry_month=12)
        self.assertEqual(credit_card.owner, user)
        self.assertEqual(credit_card.alias, 'my awesome card')
        self.assertEqual(credit_card.card_number, '1234567890123456')
        self.assertEqual(credit_card.cvc, '123')
        self.assertEqual(credit_card.expiry_year, 2032)
        self.assertEqual(credit_card.expiry_month, 12)

    def test_credit_card_creation_with_wrong_expiry_should_fail(self):
        user = User.objects.create_user(phone_number='01012341234',
                                        name='홍길동',
                                        password='thePas123Q',
                                        role=UserRole.CLIENT)
        with self.assertRaises(ValidationError):
            credit_card = CreditCard(owner=user,
                                     alias='my awesome card',
                                     card_number='1234567890123456',
                                     cvc='123',
                                     expiry_year=None,
                                     expiry_month=None)
            credit_card.full_clean()
            credit_card.save()

    def test_credit_card_creation_with_wrong_cvc_should_fail(self):
        user = User.objects.create_user(phone_number='01012341234',
                                        name='홍길동',
                                        password='thePas123Q',
                                        role=UserRole.CLIENT)
        with self.assertRaises(IntegrityError):
            credit_card = CreditCard(owner=user,
                                     alias='my awesome card',
                                     card_number='1234567890123456',
                                     cvc=None,
                                     expiry_year=2032,
                                     expiry_month=12)
            credit_card.save()

    def test_credit_card_creation_with_wrong_card_number_should_fail(self):
        """all of the codes are the same as the upper test, but the length of card_number should be 1."""
        user = User.objects.create_user(phone_number='01012341234',
                                        name='홍길동',
                                        password='thePas123Q',
                                        role=UserRole.CLIENT)
        with self.assertRaises(ValidationError):
            credit_card = CreditCard(owner=user,
                                     alias='my awesome card',
                                     card_number='1',
                                     cvc='123',
                                     expiry_year=2032,
                                     expiry_month=12)
            credit_card.full_clean()
            credit_card.save()