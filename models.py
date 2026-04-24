from django.db import models
from django.utils import timezone

class Instrument(models.Model):
    POSSIBLE_STATUS = [
        ('available', 'Available'),
        ('rented', 'Rented'),
        ('maintenance', 'Maintenance'),
    ]

    barcode = models.CharField(max_length=100, unique=True)
    name = models.CharField(max_length=200)
    category = models.CharField(max_length=100)
    status = models.CharField(max_length=20, choices=POSSIBLE_STATUS, default="available")

    def __str__(self):
        return f"{self.name} ({self.barcode}) - {self.status}"


class Customer(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.email}"


class Rental(models.Model):
    instrument = models.ForeignKey(Instrument, on_delete=models.PROTECT)
    customer = models.ForeignKey(Customer, on_delete=models.PROTECT)
    rental_date = models.DateTimeField(default=timezone.now)
    returned = models.BooleanField(default=False)
    return_date = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f"Rental of {self.instrument.name} to {self.customer.first_name} on {self.rental_date}"

    def mark_returned(self):
        """Mark the rental as returned and update the instrument status."""
        self.returned = True
        self.return_date = timezone.now()

        # Update instrument status
        self.instrument.status = 'available'
        self.instrument.save()

        # Save rental
        self.save()
