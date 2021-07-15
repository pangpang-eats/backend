from django.db import models
from django.core.validators import MinLengthValidator
from pangpangeats.settings import AUTH_USER_MODEL
from apps.common.models import BaseModel


class Restaurant(BaseModel):
    owner = models.ForeignKey(
        AUTH_USER_MODEL, null=False, on_delete=models.PROTECT
    )  # the user shouldn't be deleted instead of deativation
    name = models.CharField(max_length=40, null=False)
    picture = models.ImageField(upload_to='staticfiles/restaurant_pictures',
                                null=False)
    minimum_order_cost = models.IntegerField(null=False)
    minimum_delivery_cost = models.IntegerField(null=False)
    telephone_number = models.CharField(
        validators=(MinLengthValidator(9),
                    ),  # in case of normal numbers like: 02-123-1234
        max_length=11,  # in case of mobile numbers like: 010-1234-1234
        null=False,
    )

    description = models.TextField(null=False)
    notice = models.TextField(null=False)

    origin_information = models.TextField(null=False)
    nuturition_facts = models.TextField(null=False)
    allergens_facts = models.TextField(null=False)

    def __str__(self):  # pragma: no cover
        return f"{self.name} {self.location}"


class Location(BaseModel):
    restaurant = models.OneToOneField(Restaurant,
                                      null=False,
                                      on_delete=models.CASCADE)
    address = models.CharField(max_length=40, null=False)
    latitude = models.FloatField(null=False)
    longitude = models.FloatField(null=False)

    def __str__(self):  # pragma: no cover
        return self.address


class BusinessInformation(BaseModel):
    restaurant = models.OneToOneField(Restaurant,
                                      null=False,
                                      on_delete=models.CASCADE)
    owner_name = models.CharField(max_length=5, null=False)
    business_name = models.CharField(max_length=40, null=False)
    business_registration_number = models.CharField(
        validators=[MinLengthValidator(10)],
        max_length=10,
        null=False,
    )

    def __str__(self):  # pragma: no cover
        return self.business_name


class MenuInformation(BaseModel):
    # reference restaurant to get the user
    restaurant: Restaurant = models.ForeignKey(
        Restaurant,
        null=False,
        on_delete=models.CASCADE,
    )  # if restaurant is gone, than the menu information should be gone, too (cascade)
    name = models.CharField(max_length=20, null=False)
    description = models.CharField(max_length=100, null=False)
    picture = models.ImageField(upload_to='menu_pictures', null=False)
    price = models.PositiveIntegerField(null=False)
    is_available = models.BooleanField(default=True)

    def __str__(self):  # pragma: no cover
        return f"{self.restaurant.name} {self.name}"