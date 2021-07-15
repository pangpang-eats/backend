from django.contrib import admin
from apps.restaurant.models import BusinessInformation, Location, MenuInformation, Restaurant


class LocationInline(admin.TabularInline):
    model = Location


class BusinessInformationInline(admin.TabularInline):
    model = BusinessInformation


class MenuInformationInline(admin.StackedInline):
    model = MenuInformation


@admin.register(Restaurant)
class RestaurantAdmin(admin.ModelAdmin):
    list_display = ('owner', 'name', 'picture', 'minimum_order_cost',
                    'minimum_delivery_cost', 'telephone_number', 'description',
                    'notice', 'origin_information', 'nuturition_facts',
                    'allergens_facts')
    inlines = (LocationInline, BusinessInformationInline,
               MenuInformationInline)
