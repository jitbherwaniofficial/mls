from django.urls import path
from .views import create_property, view_property_mls,update_property,generate_mls_pdf

urlpatterns = [
    path("create-mls/", create_property, name="create_property"),
    path("property/<int:pk>/", view_property_mls, name="view_property_mls"),
    path("property/<int:pk>/edit/", update_property, name="update_property"),
    path("property/<int:pk>/pdf/", generate_mls_pdf, name="generate_mls_pdf"),
]