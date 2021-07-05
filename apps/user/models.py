from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.core.validators import MinLengthValidator
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from pangpangeats.settings import AUTH_USER_MODEL


class UserRole(models.TextChoices):
    CLIENT = "CLI", _("Client")
    STORE_OWNER = "STO", _("Store Owner")
    ETC = "ETC", _("ETC")


class UserManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self,
                    phone_number,
                    name,
                    password=None,
                    role=UserRole.CLIENT):
        """
        Creates and saves a User with the given phone_number, name and password.
        """
        if not phone_number:
            raise ValueError('Users must have an phone_number')
        user = self.model(
            phone_number=phone_number,
            name=name,
            role=role,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone_number, name, password):
        """
        Creates and saves a superuser with the given phone_number, name and password.
        """
        user = self.create_user(
            phone_number=phone_number,
            name=name,
            role=UserRole.ETC,
        )
        user.is_verified = True
        user.is_superuser = True
        user.is_staff = True
        user.is_admin = True
        user.set_password(password)
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    objects = UserManager()

    phone_number = models.CharField(
        validators=(MinLengthValidator(9),
                    ),  # in case of normal numbers like: 02-123-1234
        max_length=11,  # in case of mobile numbers like: 010-1234-1234
        unique=True,
    )
    name = models.CharField(max_length=10, null=False, blank=False)
    role = models.CharField(max_length=3,
                            choices=UserRole.choices,
                            default=UserRole.CLIENT)

    is_active = models.BooleanField(default=True)
    is_verified = models.BooleanField(
        default=False)  # is phone_number verified

    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    date_joined = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = ['name']

    class Meta:
        db_table = "pangpangeats_user"


class CreditCard(models.Model):
    owner: User = models.ForeignKey(AUTH_USER_MODEL,
                                    on_delete=models.CASCADE,
                                    null=False)
    owner_first_name = models.CharField(max_length=5, null=False, blank=False)
    owner_last_name = models.CharField(max_length=5, null=False, blank=False)
    alias = models.CharField(max_length=100, null=True, blank=True)
    card_number = models.CharField(
        validators=(MinLengthValidator(16), ),
        max_length=16,
        null=False,
        blank=False,
    )
    cvc = models.CharField(
        validators=(MinLengthValidator(3), ),
        max_length=3,
        null=False,
        blank=False,
    )
    # both should be a future than now, but not validate them on the model, but validate them in the serializer
    expiry_year = models.PositiveSmallIntegerField(null=False)
    expiry_month = models.PositiveSmallIntegerField(null=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):  # pragma: no cover
        CARD_NUMBER = self.card_number[:4] + "-****" * 3
        return f"{self.owner_last_name}{self.owner_first_name} {CARD_NUMBER}"