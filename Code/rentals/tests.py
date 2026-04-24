from django.test import TestCase
from .models import Customer, Instrument, Rental, RentalItem
from django.utils import timezone
from django.db import IntegrityError

# Class to test users, rental items, and rentals
class ModelTests(TestCase):
    def setUp(self):
        # Set up a customer user account
        self.customer = Customer.objects.create(
            first_name="John",
            last_name="Doe",
            email="JohnDoe@test.com",
            phone_number="1234567890"
        )
        # Set up an instrument item
        self.instrument = Instrument.objects.create(
            barcode="1234567890123",
            name="Fender Stratocaster",
            category="Guitar",
            status="available",
            color="Red"
        )
        # Set up a rental with dates
        self.rental = Rental.objects.create(
            customer=self.customer,
            rental_date=timezone.now().strftime("%Y-%m-%d %H:%M:%S"),
            returned=False
        )
        # Set up a rental of the instrument item
        self.rental_item = RentalItem.objects.create(
            rental=self.rental,
            instrument=self.instrument
        )

    # Testing customer model  ---------------------------------------
    def test_create_customer(self):
        self.assertEqual(self.customer.first_name, "John")
        self.assertEqual(self.customer.last_name, "Doe")
        self.assertIsNotNone(self.customer.id)
        self.assertIsInstance(self.customer.id, int)
        self.assertGreater(self.customer.id, 0)
    # Create addition customer
    def test_multiple_customers(self):
        self.customer2 = Customer.objects.create(
            first_name="Jane",
            last_name="Smith",
            email="Jane@test.com",
            phone_number="0987654321"
        )
        self.assertEqual(self.customer.first_name, "John")
        self.assertEqual(self.customer2.first_name, "Jane")
        self.assertNotEqual(self.customer.id, self.customer2.id)
        self.assertEqual(Customer.objects.count(), 2)
        self.assertEqual(self.customer.email, "JohnDoe@test.com")
        self.assertEqual(self.customer2.email, "Jane@test.com")
        self.assertNotEqual(self.customer.phone_number, self.customer2.phone_number)

    #Test made using AI to understnad IntegrityError with unique keys
    def test_same_customer_email(self):
        with self.assertRaises(IntegrityError) as context:
            Customer.objects.create(
                first_name="John",
                last_name="Doe",
                email="JohnDoe@test.com",
                phone_number="1112223333"
            )
        print(str(context.exception))
    #Test made using AI to understnad IntegrityError with unique keys
    def test_same_customer_phoneNumber(self):
        with self.assertRaises(IntegrityError) as context:
            Customer.objects.create(
                first_name="John",
                last_name="Doe",
                email="JohnDoesCode@test.com",
                phone_number="1234567890"
            )
        print(str(context.exception))


    # Testing instrument model  ---------------------------------------
    def test_create_instrument(self):
        self.assertEqual(self.instrument.barcode, "1234567890123")
        self.assertEqual(self.instrument.name, "Fender Stratocaster")
        self.assertEqual(self.instrument.category, "Guitar")
        self.assertEqual(self.instrument.status, "available")
        self.assertEqual(self.instrument.color, "Red")
        self.assertIsNotNone(self.instrument.id)
    # Test additional instrument items
    def test_multiple_instruments(self):
        self.instrument2 = Instrument.objects.create(
            barcode="9876543210987",
            name="Gibson Les Paul",
            category="Guitar",
            status="available",
            color="red"
        )
        self.assertEqual(self.instrument.barcode, "1234567890123")
        self.assertEqual(self.instrument2.barcode, "9876543210987")
        self.assertNotEqual(self.instrument.id, self.instrument2.id)
        self.assertEqual(Instrument.objects.count(), 2)
        self.assertEqual(self.instrument.name, "Fender Stratocaster")
        self.assertEqual(self.instrument2.name, "Gibson Les Paul")

    #Test made using AI to understnad IntegrityError with unique keys
    def test_same_instrument_barcode(self):
        with self.assertRaises(IntegrityError) as context:
            Instrument.objects.create(
                barcode="1234567890123",
                name="Fender Stratocaster",
                category="Guitar",
                status="available",
                color="Red"
            )
        print(str(context.exception))
    # Test duplicate instrument items
    def test_two_same_instrument_different_barcodes(self):
        self.instrument2 = Instrument.objects.create(
            barcode="246810121618",
            name="Fender Stratocaster",
            category="Guitar",
            status="available",
            color="Blue"
        )
        self.assertEqual(Instrument.objects.count(), 2)
        self.assertEqual(self.instrument.name, "Fender Stratocaster")
        self.assertEqual(self.instrument2.name, "Fender Stratocaster")
        self.assertNotEqual(self.instrument.barcode, self.instrument2.barcode)
        self.assertNotEqual(self.instrument.id, self.instrument2.id)
    # Test status change of an instrument item in inventory
    def test_instrument_status_change(self):
        self.instrument4 = Instrument.objects.create(
            barcode="3691215182124",
            name="Yamaha motif 8",
            category="Keyboard",
            status="available",
            color="Black"
        )
        self.assertEqual(self.instrument4.status, "available")
        # The keyboard gets rented
        self.instrument4.status = "rented"
        # saves the change to the database
        self.instrument4.save()
        # retrieves the updated instrument from the database
        updated_instrument = Instrument.objects.get(id=self.instrument4.id)
        self.assertEqual(updated_instrument.status, "rented")

    # Testing rental model  ---------------------------------------
    def test_create_rental(self):
        self.assertEqual(self.rental.customer, self.customer)
        self.assertEqual(self.rental.rental_date, timezone.now().strftime("%Y-%m-%d %H:%M:%S"))
        self.assertEqual(self.rental.returned, False)
        self.assertEqual(self.rental.return_date, None)
        self.assertIsNotNone(self.rental.id)
    # Test additional rentals for one customer
    def test_multiple_rentals_same_customer(self):
        self.rental2 = Rental.objects.create(
            customer=self.customer,
            rental_date=timezone.now().strftime("%Y-%m-%d %H:%M:%S"),
            returned=False
        )
        self.assertEqual(self.rental.customer, self.customer)
        self.assertEqual(self.rental2.customer, self.customer)
        self.assertNotEqual(self.rental.id, self.rental2.id)
        self.assertEqual(Rental.objects.count(), 2)
    # Test returning an item
    def test_rental_return(self):
        # rental is returned
        self.rental.returned = True
        # return date is set to current date and time
        self.rental.return_date = timezone.now().strftime("%Y-%m-%d %H:%M:%S")
        # saves the changes to the database
        self.rental.save()
        # retrieves the updated rental from the database
        updated_rental = Rental.objects.get(id=self.rental.id)
        self.assertEqual(updated_rental.returned, True)
        self.assertEqual(updated_rental.return_date, timezone.now().strftime("%Y-%m-%d %H:%M:%S"))

    # Testing rental item model  ---------------------------------------
    def test_create_rental_item(self):
        self.assertEqual(self.rental_item.rental, self.rental)
        self.assertEqual(self.rental_item.instrument, self.instrument)
        self.assertIsNotNone(self.rental_item.id)

    def test_multiple_rental_items_same_rental(self):
        self.instrument2 = Instrument.objects.create(
            barcode="9876543210987",
            name="Gibson Les Paul",
            category="Guitar",
            status="available",
            color="red"
        )
        self.rental_item2 = RentalItem.objects.create(
            rental=self.rental,
            instrument=self.instrument2
        )
        # the first rental item which holds the instruments for the rental
        # is in the correct rental
        self.assertEqual(self.rental_item.rental, self.rental)
        self.assertEqual(self.rental_item.instrument, self.instrument)
        # the second rental item which holds the second instrument for the rental
        # Now the rental should have two rental items (instruments) linked to same rental
        self.assertEqual(self.rental_item2.rental, self.rental)
        self.assertNotEqual(self.rental_item.id, self.rental_item2.id)
        self.assertEqual(RentalItem.objects.count(), 2)

        items = RentalItem.objects.filter(rental=self.rental)
        for item in items:
            self.assertEqual(item.rental, self.rental)
            print(item.instrument.name)
            self.assertIn(item.instrument.name, ["Fender Stratocaster", "Gibson Les Paul"])

        self.instrument4 = Instrument.objects.create(
            barcode="3691215182124",
            name="Yamaha motif 8",
            category="Keyboard",
            status="available",
            color="Black"
        )
        self.rental_item3 = RentalItem.objects.create(
            rental=self.rental,
            instrument=self.instrument4
        )
        self.assertEqual(self.rental_item3.rental, self.rental)
        self.assertEqual(self.rental_item3.instrument, self.instrument4)
        self.assertNotEqual(self.rental_item3.id, self.rental_item.id)
        self.assertNotEqual(self.rental_item3.id, self.rental_item2.id)
        self.assertEqual(RentalItem.objects.count(), 3)
        new_items = RentalItem.objects.filter(rental=self.rental)
        for item in new_items:
            self.assertEqual(item.rental, self.rental)
            print(item.instrument.name)
            self.assertIn(item.instrument.name, ["Fender Stratocaster", "Gibson Les Paul", "Yamaha motif 8"])
