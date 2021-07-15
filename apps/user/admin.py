from django.contrib import admin
from nested_inline.admin import NestedModelAdmin, NestedStackedInline, NestedTabularInline
from apps.restaurant.models import BusinessInformation, Location, MenuInformation, Restaurant
from apps.credit_card.models import CreditCard
from apps.user.models import User


class RestaurantNestedInline(NestedStackedInline):
    model = Restaurant

    class LocationNestedInline(NestedTabularInline):
        model = Location
        fk_name = 'restaurant'
        extra = 1

    class BusinessInformationNestedInline(NestedTabularInline):
        model = BusinessInformation
        fk_name = 'restaurant'
        extra = 1

    class MenuInformationNestedInline(NestedStackedInline):
        model = MenuInformation
        fk_name = 'restaurant'
        extra = 1

    inlines = [
        LocationNestedInline, BusinessInformationNestedInline,
        MenuInformationNestedInline
    ]


class CreditCardInline(admin.StackedInline):
    model = CreditCard


@admin.register(User)
class UserAdmin(NestedModelAdmin):
    list_display = ('phone_number', 'name', 'role', 'date_joined')
    inlines = (CreditCardInline, RestaurantNestedInline)
