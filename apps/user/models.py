from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.core.validators import MinLengthValidator
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin


class UserRole(models.TextChoices):
    CLIENT = "CLI", _("Client")
    STORE_OWNER = "STO", _("Store Owner")
    ETC = "ETC", _("ETC")


class UserManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self,
                    phone_number,
                    nickname,
                    password=None,
                    role=UserRole.CLIENT):
        """
        Creates and saves a User with the given phone_number, nickname and password.
        """
        if not phone_number:
            raise ValueError('Users must have an phone_number')
        user = self.model(
            phone_number=phone_number,
            nickname=nickname,
            role=role,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone_number, password):
        """
        Creates and saves a superuser with the given phone_number, nickname and password.
        """
        user = self.create_user(
            phone_number=phone_number,
            nickname=f"admin {phone_number}",
            role=UserRole.ETC,
        )
        user.is_verified = True
        user.is_superuser = True
        user.is_staff = True
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
    nickname = models.CharField(max_length=40)
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

    class Meta:
        db_table = "pangpangeats_user"