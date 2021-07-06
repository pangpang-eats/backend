from django.contrib import admin
from apps.credit_card.models import CreditCard
from apps.user.models import User


class CreditCardInline(admin.StackedInline):
    model = CreditCard


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('phone_number', 'name', 'role', 'date_joined')
    inlines = (CreditCardInline, )
