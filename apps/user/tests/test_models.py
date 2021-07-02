from django.test import TestCase
from django.db.utils import DataError
from django.core.exceptions import ValidationError
from apps.user.models import UserRole, User


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
