from django.urls import path
from . import views

urlpatterns = [
    # Rental URLs
    path('scan/', views.scan_barcode, name='scan_barcode'),
    # Instrument URLs
    path('instruments/', views.instrument_list, name='instrument_list'),
    path('instruments/add/', views.add_instrument, name='add_instrument'),
    path('instrument/<int:instrument_id>/', views.instrument_detail, name='instrument_detail'),
    # Customer URLs
    path('customers/', views.customer_list, name='customer_list'),
    path('customers/add/', views.add_customer, name='add_customer'),
    # Rental URLs
    path('rentals/', views.rental_list, name='rental_list'),
    path("rental/create/", views.create_rental, name="create_rental"),
    path("rental/cart/add/<int:instrument_id>/", views.add_rental_cart, name="add_rental_cart"),
    path("rental/cart/remove/<int:instrument_id>/", views.remove_rental_cart, name="remove_rental_cart"),
    path("rental/return/<int:rental_id>/", views.return_rental, name="return_rental"),
    

]
