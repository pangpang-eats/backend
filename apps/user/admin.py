from django.contrib import admin
from . import models


class CreditCardInline(admin.StackedInline):
    model = models.CreditCard


@admin.register(models.User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('phone_number', 'name', 'role', 'date_joined')
    inlines = (CreditCardInline, )
