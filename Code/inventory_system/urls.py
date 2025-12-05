from django.contrib import admin
from django.urls import path, include
from rentals import views

urlpatterns = [
    path('admin/', admin.site.urls), # This runs through admin interface

    # Homepage → scan page
    path('', views.scan_barcode, name='home'),

    # App routes
    path('', include('rentals.urls')), #sends all website paths to the rentals app
]
