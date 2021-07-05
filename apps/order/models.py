import typing
from django.db import models
from pangpangeats.settings import AUTH_USER_MODEL
from apps.user.models import CreditCard, User
from apps.store.models import MenuInformation


class Selection(models.Model):
    orderer: User = models.ForeignKey(
        AUTH_USER_MODEL, on_delete=models.PROTECT
    )  # nullable becuase of on_delete option, but should required=True at the serializer
    # the user shouldn't be deleted instead of deativation
    menu: MenuInformation = models.ForeignKey(
        MenuInformation, null=True, on_delete=models.SET_NULL
    )  # nullable becuase of on_delete option, but should required=True at the serializer
    # cascade here is not allowed to keep model Order
    # the possible cases of menu deletion are:
    # 1. the owner deletes the store, and so as the menu (because of the cascade) -> the menu here set to null
    # 2. the owner deletes a menu (removing menus should be allowed) -> the menu here set to null

    amount = models.PositiveSmallIntegerField(default=1)
    request = models.CharField(max_length=100, null=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):  # pragma: no cover
        return f"{self.orderer.name} {self.menu.name}"


class Order(models.Model):
    # reference one of selections to get the user (in one order, the users (which is the field orderer) from the selections are the same)
    # the min length of selections should be 1
    selections: typing.List[Selection] = models.ManyToManyField(Selection)
    total_cost = models.PositiveIntegerField(null=False)

    is_paid = models.BooleanField(default=False)
    purchased_credit_card: CreditCard = models.ForeignKey(
        CreditCard, null=True, on_delete=models.SET_NULL
    )  # nullable becuase of on_delete option, but should required=True at the serializer
    is_canceled = models.BooleanField(default=False)
    is_delivered = models.BooleanField(default=False)

    request = models.CharField(max_length=50, null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):  # pragma: no cover
        return f"{self.orderer.name} {self.total_cost}"