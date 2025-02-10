from django.contrib import admin

from .models import BasicNeed, MLSReport, Room

# Register your models here.

admin.site.register(MLSReport)
admin.site.register(BasicNeed)
admin.site.register(Room)
