from django.db import models
from django.core.validators import MinLengthValidator
from apps.user.models import User
from pangpangeats.settings import AUTH_USER_MODEL
from apps.common.validators import numeric_validator


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
        validators=(
            MinLengthValidator(3),
            numeric_validator,
        ),
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