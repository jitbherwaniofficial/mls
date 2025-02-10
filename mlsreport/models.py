from django.db import models
from django.urls import reverse
from django import forms
from django.views.generic import CreateView, DetailView, View
from django.http import HttpResponse
from django.contrib.auth.models import User

class MLSReport(models.Model):
    detached_choices = [
        ("detached", "Detached"),
        ("undetached", "Undetached"),
    ]

    direction_choices = [
        ("north", "North"),
        ("east", "East"),
        ("south", "South"),
        ("west", "West"),
    ]

    contact_after_expiry_choices = [
        ("Y", "Yes"),
        ("N", "No"),
    ]

    spis_choices = [
        ("Y", "Yes"),
        ("N", "No"),
    ]

    family_room_choices = [
        ("Y", "Yes"),
        ("N", "No"),
    ]

    tag_choices = [
        ("new", "New"),
        ("old", "Old"),
    ]

    zone_choices = [
        ("west zone", "West Zone"),
        ("south zone", "South Zone"),
        ("east zone", "East Zone"),
        ("north zone", "North Zone"),
        ("municiple", "Municipal"),
        ("private", "Private"),
        ("unknown", "Unknown"),
        ("sewers", "Sewers"),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Add this field
    property_image = models.FileField(upload_to='property_images/', blank=True, null=True)
    property_address = models.CharField(max_length=255)
    tag = models.CharField(max_length=5, choices=tag_choices)
    postal_code_address = models.CharField(max_length=100)
    taxes = models.CharField(max_length=10, blank=True, null=True)
    taxes_year = models.IntegerField()
    lot_plan = models.CharField(max_length=100, blank=True, null=True)
    spis = models.CharField(max_length=5, choices=spis_choices)
    no_of_rooms = models.CharField(max_length=5, blank=True, null=True)
    bedrooms = models.CharField(max_length=5)
    washrooms = models.CharField(max_length=5)
    parkings = models.CharField(max_length=5)
    detached = models.CharField(max_length=20, choices=detached_choices)
    link = models.CharField(max_length=10, choices=direction_choices)
    front_on = models.CharField(max_length=10, choices=direction_choices)
    acre = models.CharField(max_length=20, blank=True, null=True)
    dir_cross_st = models.CharField(max_length=255, blank=True, null=True)
    irreg = models.CharField(max_length=100)
    client_desc = models.TextField()
    extras = models.TextField()
    mls_number = models.CharField(max_length=10)
    holdover = models.IntegerField()
    pin_number = models.CharField(max_length=8)
    possession_remarks = models.CharField(max_length=10)
    arn_number = models.CharField(max_length=8)
    occupancy = models.CharField(max_length=10)
    contact_after_expiry = models.CharField(max_length=1, choices=contact_after_expiry_choices)

    # Many-to-Many Fields
    basic_needs = models.ManyToManyField('BasicNeed')

    kitchens = models.CharField(max_length=20)
    family_room = models.CharField(max_length=5, choices=family_room_choices)
    basement = models.CharField(max_length=20)
    fireplace_stv = models.CharField(max_length=20)
    heat = models.CharField(max_length=20)
    air_conditioning = models.CharField(max_length=20)
    central_vac = models.CharField(max_length=20)
    approximate_age = models.CharField(max_length=20)
    approximate_sqft = models.CharField(max_length=20)
    assesment = models.CharField(max_length=20)
    potl = models.CharField(max_length=20)
    elevator_lift = models.CharField(max_length=20)
    laundry_lev = models.CharField(max_length=20)
    physical_hdcp_eqp = models.CharField(max_length=20)
    exterior = models.CharField(max_length=20)
    drive = models.CharField(max_length=20)
    garage_parking_space = models.CharField(max_length=20)
    total_parkings = models.CharField(max_length=20)
    uffi = models.CharField(max_length=20)
    pool = models.CharField(max_length=20)
    energy_certificate = models.CharField(max_length=20)
    certificate_level = models.CharField(max_length=20, blank=True, null=True)
    green_pis = models.CharField(max_length=20)
    prop_feat = models.CharField(max_length=20)

    def get_absolute_url(self):
        return reverse('view-report', args=[str(self.id)])
    
    def __str__(self):
        return self.property_address

class BasicNeed(models.Model):
    title = models.CharField(max_length=100)
    zone = models.CharField(max_length=20, choices=MLSReport.zone_choices)
    icon = models.FileField(upload_to='basic_needs_icons/', blank=True, null=True)

    def __str__(self):
        return self.title

class Room(models.Model):
    room_title = models.CharField(max_length=100)
    room_level = models.CharField(max_length=20, choices=[("main", "Main"), ("second", "Second"), ("basement", "Basement")])
    room_length = models.DecimalField(max_digits=5, decimal_places=2)
    room_width = models.DecimalField(max_digits=5, decimal_places=2)
    room_description = models.TextField()
    report = models.ForeignKey(MLSReport, on_delete=models.CASCADE, related_name="rooms")

    def __str__(self):
        return self.room_title
    

# author_names = book.authors.values_list('name', flat=True)  # Returns a list of names
# print(author_names)  # ['Author 1', 'Author 2']
