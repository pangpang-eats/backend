from django.test import TestCase
from django.db.utils import DataError, IntegrityError
from django.core.exceptions import ValidationError
from apps.user.models import UserRole, User, CreditCard


class UserCreationTest(TestCase):
    def test_normal_user_creation_with_proper_phone_number_should_success(
            self):
        user = User.objects.create_user(phone_number='01012341234',
                                        nickname='mengmota',
                                        password='thePas123Q',
                                        role=UserRole.CLIENT)
        self.assertEqual(user.phone_number, '01012341234')
        self.assertEqual(user.nickname, 'mengmota')
        self.assertEqual(user.role, UserRole.CLIENT)

    def test_user_creation_with_9_length_of_phone_number_should_success(self):
        user = User.objects.create_user(phone_number='021231234',
                                        nickname='mengmota',
                                        password='thePas123Q',
                                        role=UserRole.CLIENT)
        self.assertEqual(user.phone_number, '021231234')
        self.assertEqual(user.nickname, 'mengmota')
        self.assertEqual(user.role, UserRole.CLIENT)

    def test_store_owner_user_creation_with_proper_phone_number_should_success(
            self):
        user = User.objects.create_user(phone_number='01012341234',
                                        nickname='mengmota',
                                        password='thePas123Q',
                                        role=UserRole.STORE_OWNER)
        self.assertEqual(user.phone_number, '01012341234')
        self.assertEqual(user.nickname, 'mengmota')
        self.assertEqual(user.role, UserRole.STORE_OWNER)

    def test_user_creation_without_phone_number_should_fail(self):
        with self.assertRaises(ValueError):
            User.objects.create_user(phone_number=None,
                                     nickname='mengmota',
                                     password='thePas123Q',
                                     role=UserRole.CLIENT)

    def test_user_creation_with_too_long_phone_number_should_fail(self):
        with self.assertRaises(DataError):
            User.objects.create_user(phone_number='123456789123',
                                     nickname='mengmota',
                                     password='thePas123Q',
                                     role=UserRole.CLIENT)

    def test_user_creation_with_too_short_phone_number_should_fail(self):
        with self.assertRaises(ValidationError):
            user = User(phone_number='1',
                        nickname='mengmota',
                        password='thePas123Q',
                        role=UserRole.CLIENT)
            user.full_clean()

    def test_create_superuser_should_success(self):
        User.objects.create_superuser(phone_number='01012341234',
                                      password='thePas123Q')


class CreditCardTest(TestCase):
    def test_credit_card_creation_with_new_user_should_success(self):
        user = User.objects.create_user(phone_number='01012341234',
                                        nickname='mengmota',
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
        self.assertEqual(str(credit_card), "1234-****-****-****")

    def test_credit_card_creation_with_wrong_expiry_should_fail(self):
        user = User.objects.create_user(phone_number='01012341234',
                                        nickname='mengmota',
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
                                        nickname='mengmota',
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
                                        nickname='mengmota',
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