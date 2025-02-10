from django.urls import path
from . import views

urlpatterns = [
    path('new/', views.create_mls_report, name='create_mls_report'),
    path('edit/<int:pk>/', views.edit_mls_report, name='edit_mls_report'),
    path('<int:pk>/', views.view_mls_report, name='view_mls_report'),
    path('<int:pk>/download/', views.generate_mls_report, name='generate_mls_report'),
] 