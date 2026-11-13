from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('properties/', views.property_list, name='property_list'),
    path('properties/<int:property_id>/', views.property_detail, name='property_detail'),
    path('register-client/', views.client_register, name='client_register'),
    path('properties/<int:property_id>/inquiry/', views.property_inquiry, name='property_inquiry'),
]