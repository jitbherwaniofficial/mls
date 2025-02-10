# Register your models here.
from django.contrib import admin
from .models import Realtor, Property, ListingInfo, PropertyInfo, Room, Washroom

# Realtor Admin
@admin.register(Realtor)
class RealtorAdmin(admin.ModelAdmin):
    list_display = ('name', 'designation')
    search_fields = ('name',)
    ordering = ('name',)

# Inline classes for related models (ListingInfo & PropertyInfo)
class ListingInfoInline(admin.StackedInline):
    model = ListingInfo
    extra = 0

class PropertyInfoInline(admin.StackedInline):
    model = PropertyInfo
    extra = 0

class RoomInline(admin.TabularInline):
    model = Room
    extra = 1

class WashroomInline(admin.TabularInline):
    model = Washroom
    extra = 1

# Property Admin
@admin.register(Property)
class PropertyAdmin(admin.ModelAdmin):
    list_display = ('address_1', 'status', 'price', 'realtor', 'title')
    list_filter = ('status', 'condition', 'realtor')
    search_fields = ('title', 'address_1', 'realtor__name')
    ordering = ('-price',)
    inlines = [ListingInfoInline, PropertyInfoInline, RoomInline, WashroomInline]

# Registering other models separately (if needed)
@admin.register(ListingInfo)
class ListingInfoAdmin(admin.ModelAdmin):
    list_display = ('property', 'pin_number', 'taxes', 'tax_year', 'status')
    search_fields = ('property__title', 'pin_number')

@admin.register(PropertyInfo)
class PropertyInfoAdmin(admin.ModelAdmin):
    list_display = ('property', 'approx_age', 'lot_size', 'square_feet', 'drive')
    search_fields = ('property__title', 'approx_age')

@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ('property', 'name', 'level')
    search_fields = ('property__title', 'name')
    list_filter = ('level',)

@admin.register(Washroom)
class WashroomAdmin(admin.ModelAdmin):
    list_display = ('property', 'pieces', 'level')
    list_filter = ('level', 'pieces')
