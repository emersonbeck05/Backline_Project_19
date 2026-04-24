from django.db import models

# This class represents a musical instrument available for rent
class Instrument(models.Model):
    id = models.AutoField(primary_key=True) # Instrument ID
    barcode = models.CharField(max_length=255, unique=True) # Unique barcode for the instrument
    name = models.CharField(max_length=255) # Name of the instrument
    category = models.CharField(max_length=255) # Category of the instrument
    status = models.CharField(max_length=50, default="available") # Status of the instrument (e.g., available, rented)
    color = models.TextField(max_length=50, blank=True, null=True)  # Color of the instrument (TEXT in SQLite)
    class Meta:
        db_table = "instrument"

    def __str__(self):
        return f"{self.name} ({self.barcode})"

# This class represents a customer who rents instruments
class Customer(models.Model):
    id = models.AutoField(primary_key=True) # Customer ID
    first_name = models.CharField(max_length=255) #customers First name
    last_name = models.CharField(max_length=255) # Customer's last name
    email = models.EmailField(unique=True) #customers email
    phone_number = models.CharField(max_length=20, null=True, blank=True, unique=True) #customers phone number

    class Meta: #used to define the database table name
        db_table = "customer"

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

# This class represents the rental transaction
class Rental(models.Model):
    id = models.AutoField(primary_key=True) # Rental ID

    customer = models.ForeignKey( #customer who rented the instrument(s)
        Customer,
        on_delete=models.CASCADE, #if the customer is deleted, delete their rentals too
        db_column="customer_id", #specifies the column name in the database
    )

    rental_date = models.CharField(max_length=50) #set when the rental was made
    returned = models.BooleanField(default=False) #whether the rental has been returned
    return_date = models.CharField(max_length=50, null=True, blank=True) #set when the rental was returned

    class Meta: #used to define the database table name
        db_table = "rental"

    def __str__(self): #string representation of the rental
        return f"Rental #{self.id}"


# This class represents individual items within a rental
class RentalItem(models.Model):
    id = models.AutoField(primary_key=True) # RentalItem ID
    # Foreign key to the rental this item belongs to
    rental = models.ForeignKey(Rental, on_delete=models.CASCADE, db_column="rental_id")
    # Foreign key to the instrument being rented
    instrument = models.ForeignKey(Instrument, on_delete=models.CASCADE, db_column="instrument_id")
    

    class Meta: #used to define the database table name
        db_table = "rentalitem"

    def __str__(self):
        return f"Item for Rental #{self.rental_id}"


