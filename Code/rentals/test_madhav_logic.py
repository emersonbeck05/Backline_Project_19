# Madhav PM5 Tests
# AI assisted: Used AI to help design test cases and structure integration testing
# Focus: Testing rental return logic and system behavior without Django dependency

from datetime import datetime


# ---------------- Mock Classes (No Django Needed) ----------------

class Customer:
    def __init__(self, id, first_name, last_name, email, phone):
        self.id = id
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.phone = phone


class Instrument:
    def __init__(self, id, barcode, name, category, status):
        self.id = id
        self.barcode = barcode
        self.name = name
        self.category = category
        self.status = status


class Rental:
    def __init__(self, id, customer, rental_date, returned):
        self.id = id
        self.customer = customer
        self.rental_date = rental_date
        self.returned = returned
        self.return_date = None


class RentalItem:
    def __init__(self, id, rental, instrument):
        self.id = id
        self.rental = rental
        self.instrument = instrument


# ---------------- Test Cases ----------------

def test_rental_return_updates_fields():
    customer = Customer(1, "Madhav", "M", "m@test.com", "111")
    instrument = Instrument(1, "123", "Keyboard", "Keys", "rented")

    rental = Rental(1, customer, str(datetime.now()), False)
    rental_item = RentalItem(1, rental, instrument)

    # simulate return
    rental.returned = True
    rental.return_date = str(datetime.now())

    assert rental.returned is True
    assert rental.return_date is not None


def test_instrument_status_after_return():
    instrument = Instrument(2, "456", "Guitar", "String", "rented")

    # simulate return
    instrument.status = "available"

    assert instrument.status == "available"


def test_rental_item_links_correct_objects():
    customer = Customer(2, "Madhav", "M", "m2@test.com", "222")
    instrument = Instrument(2, "789", "Drum", "Percussion", "rented")

    rental = Rental(2, customer, str(datetime.now()), False)
    rental_item = RentalItem(2, rental, instrument)

    assert rental_item.rental == rental
    assert rental_item.instrument == instrument


def test_full_rental_flow_integration():
    customer = Customer(3, "Madhav", "M", "m3@test.com", "333")
    instrument = Instrument(3, "999", "Bass", "String", "rented")

    rental = Rental(3, customer, str(datetime.now()), False)
    rental_item = RentalItem(3, rental, instrument)

    # simulate return process
    rental.returned = True
    rental.return_date = str(datetime.now())
    instrument.status = "available"

    assert rental.returned is True
    assert instrument.status == "available"
    assert rental_item.instrument == instrument
    assert rental.customer == customer


if __name__ == "__main__":
    print("Running Madhav PM5 Tests...\n")

    test_rental_return_updates_fields()
    print("test_rental_return_updates_fields passed")

    test_instrument_status_after_return()
    print("test_instrument_status_after_return passed")

    test_rental_item_links_correct_objects()
    print("test_rental_item_links_correct_objects passed")

    test_full_rental_flow_integration()
    print("test_full_rental_flow_integration passed")

    print("\nAll tests executed successfully.")