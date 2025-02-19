from django.db import models
from django.contrib.auth.models import User

# Create your models here.

from django.db import models
import json

class Realtor(models.Model):
    name = models.CharField(max_length=255)
    designation = models.CharField(max_length=100)

    class Meta:
        verbose_name = "Realtor"
        verbose_name_plural = "Realtors"

    def __str__(self):
        return self.name    

class Property(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE) 
    realtor = models.ForeignKey(Realtor, on_delete=models.CASCADE, related_name="properties")
    address_1 = models.CharField(max_length=255)
    address_2 = models.CharField(max_length=255, blank=True, null=True)
    address_3 = models.CharField(max_length=255, blank=True, null=True)
    address_4 = models.CharField(max_length=50, blank=True, null=True)
    title = models.CharField(max_length=255)
    condition = models.CharField(max_length=50)
    status = models.CharField(max_length=50)
    price = models.CharField(max_length=50)
    taxes = models.CharField(max_length=50)
    features = models.JSONField()  # Stores bed, bath, parking, etc.
    main_image = models.URLField(max_length=1500)
    client_remark = models.TextField()
    extras = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name = "Property"
        verbose_name_plural = "Properties"

    def __str__(self):
        return f"{self.address_1}"

class ListingInfo(models.Model):
    property = models.OneToOneField(Property, on_delete=models.CASCADE, related_name="listing_info")
    pin_number = models.CharField(max_length=100)
    taxes = models.CharField(max_length=50)
    tax_year = models.CharField(max_length=10)
    legal_description = models.TextField()
    status = models.CharField(max_length=50)
    possession_remarks = models.CharField(max_length=255, blank=True, null=True)
    seller_info = models.CharField(max_length=10)

    class Meta:
        verbose_name = "Listing Information"
        verbose_name_plural = "Listing Information"

    def __str__(self):
        return f"Listing {self.pin_number}"

class PropertyInfo(models.Model):
    property = models.OneToOneField(Property, on_delete=models.CASCADE, related_name="property_info")
    approx_age = models.CharField(max_length=50)
    fronting_on = models.CharField(max_length=50)
    lot_size = models.CharField(max_length=100)
    square_feet = models.CharField(max_length=50)
    drive = models.CharField(max_length=100)
    total_parking_spaces = models.IntegerField()
    pool = models.CharField(max_length=50, blank=True, null=True)
    air_conditioning = models.CharField(max_length=50)
    heating_source = models.CharField(max_length=50)
    heating_type = models.CharField(max_length=50)
    water = models.CharField(max_length=50)
    sewers = models.CharField(max_length=50)
    dir_cross_st = models.CharField(max_length=250)
    parking_drive_space = models.CharField(max_length=50)
    HST_applicable_to_sale_price = models.CharField(max_length=50)
    laundary_level = models.CharField(max_length=50)
    lot_size_source = models.CharField(max_length=50)
    area = models.CharField(max_length=50)
    municipality = models.CharField(max_length=50)
    community = models.CharField(max_length=100)
    rooms = models.CharField(max_length=50)
    bedrooms = models.CharField(max_length=50)
    washrooms = models.CharField(max_length=50)
    kitchens = models.CharField(max_length=50)
    exteriors = models.CharField(max_length=50)
    roof = models.CharField(max_length=50)
    foundation = models.CharField(max_length=50)
    garage_type = models.CharField(max_length=50)
    garage_parking_spaces = models.CharField(max_length=50)
    basement = models.CharField(max_length=50)
    water_front = models.CharField(max_length=50)


    class Meta:
        verbose_name = "Property Information"
        verbose_name_plural = "Property Information"

    def __str__(self):
        return f"Info for {self.property}"

class Room(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name="rooms")
    name = models.CharField(max_length=100)
    level = models.CharField(max_length=50)
    dimensions = models.JSONField()
    notes = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name = "Room"
        verbose_name_plural = "Rooms"

    def __str__(self):
        return f"{self.name} in {self.property.title}"

class Washroom(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name="washrooms")
    pieces = models.IntegerField()
    level = models.CharField(max_length=50)

    class Meta:
        verbose_name = "Washroom"
        verbose_name_plural = "Washrooms"

    def __str__(self):
        return f"{self.pieces}-piece washroom in {self.property.title}"
