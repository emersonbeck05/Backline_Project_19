from django.shortcuts import render, redirect
from django.db import IntegrityError
from datetime import datetime
from .models import Instrument, Customer, Rental, RentalItem
from . import services


# ---------------------------------------------------------
# SCAN BARCODE
# ---------------------------------------------------------
# this function handles the scanning of barcodes for renting and returning instruments
def scan_barcode(request):
    message = "" # Initialize an empty message string

    if request.method == "POST": # Check if the request method is POST
        barcode = request.POST.get("barcode", "").strip() # Get the barcode from the POST data and strip whitespace
        action = request.POST.get("action") # Get the action (rent or return) from the POST data

        try:
            instrument = Instrument.objects.get(barcode=barcode) # Retrieve the instrument with the given barcode

            if action == "rent": # If the action is to rent the instrument
                if instrument.status == "available": # Check if the instrument is available
                    instrument.status = "rented" # change status to rented
                    message = f"{instrument.name} rented successfully." # Set success message
                else:
                    message = f"{instrument.name} is not available." # Set not available message

            elif action == "return": # If the action is to return the instrument
                if instrument.status == "rented": # Check if the instrument is currently rented
                    instrument.status = "available" # Change status to available
                    message = f"{instrument.name} returned successfully." # Set success message
                else:
                    message = f"{instrument.name} cannot be returned." # Set cannot be returned message

            instrument.save() # Save the changes to the instrument

        except Instrument.DoesNotExist:
            message = "Instrument not found."

    return render(request, "rentals/scan.html", {"message": message}) # Render the scan template with the message


# ---------------------------------------------------------
# INSTRUMENT LIST
# ---------------------------------------------------------
# this function displays a list of all instruments
def instrument_list(request):
    instruments = services.get_all_instruments()

    # Detect rental mode flag
    rental_mode = request.GET.get("rental_mode", "0")

    return render(request, 'rentals/instrument_list.html', {
        'instruments': instruments,
        'rental_mode': rental_mode,
    })





# ---------------------------------------------------------
# INSTRUMENT DETAIL
# ---------------------------------------------------------
# this function displays the details of a specific instrument
def instrument_detail(request, instrument_id):
    try:
        instrument = Instrument.objects.get(id=instrument_id)
        return render(request, "rentals/instrument_detail.html", {"instrument": instrument})
    except Instrument.DoesNotExist:
        return render(request, "rentals/instrument_detail.html", {"error": "Instrument not found"})


# ---------------------------------------------------------
# ADD INSTRUMENT
# ---------------------------------------------------------
# this function handles adding a new instrument to the inventory
def add_instrument(request):
    error = None

    if request.method == "POST":
        name = request.POST.get("name")
        category = request.POST.get("category")
        barcode = request.POST.get("barcode")
        color = request.POST.get("color")

        ok, error = services.add_instrument( # Call the service to add a new instrument
            barcode=barcode,
            name=name,
            category=category,
            color=color,
            status="available",
        ) # Call the service to add a new instrument

        if ok:
            return redirect("instrument_list")

    return render(request, "rentals/add_instrument.html", {"error": error})



# ---------------------------------------------------------
# CUSTOMER LIST & ADD CUSTOMER
# ---------------------------------------------------------
# this function displays a list of all customers
def customer_list(request):
    customers = Customer.objects.all()
    return render(request, "rentals/customer_list.html", {"customers": customers})

# this function handles adding a new customer
def add_customer(request):
    error = None
    if request.method == "POST":
        try:
            Customer.objects.create(
                first_name=request.POST.get("first_name"),
                last_name=request.POST.get("last_name"),
                email=request.POST.get("email"),
                phone_number=request.POST.get("phone_number")
            )
            return redirect("customer_list")

        except IntegrityError:
            error = "A customer with that email already exists."

    return render(request, "rentals/add_customer.html", {"error": error})


# ---------------------------------------------------------
# RENTAL LIST
# ---------------------------------------------------------
# this function displays a list of all rentals
def rental_list(request):
    rentals = Rental.objects.all()
    return render(request, "rentals/rental_list.html", {"rentals": rentals})

# this function processes the return of a rental
def return_rental(request, rental_id):
    services.return_full_rental(rental_id)
    return redirect("rental_list")


# ---------------------------------------------------------
# CREATE RENTAL (multi-instrument cart)
# ---------------------------------------------------------
# this function handles creating a rental with multiple instruments in a cart
def create_rental(request):
    # Cart of instrument IDs stored in session
    cart = request.session.get("rental_cart", [])

    # Instruments currently in the cart
    instruments = services.get_instruments_for_ids(cart)

    # Customers for dropdown
    customers = services.get_customers_dropdown()

    if request.method == "POST":
        # Existing customer choice
        customer_id = request.POST.get("customer_id") or None

        # New customer data
        new_first = request.POST.get("new_first_name") or ""
        new_last = request.POST.get("new_last_name") or ""
        new_email = request.POST.get("new_email") or ""
        new_phone = request.POST.get("new_phone") or ""

        # If any new-customer field is filled, create a new customer
        if new_first or new_last or new_email or new_phone:
            if not new_first or not new_last:
                return render(request, "rentals/create_rental.html", {
                    "customers": customers,
                    "instruments": instruments,
                    "error": "New customers must have FIRST and LAST name."
                })

            customer_id, err = services.create_customer( # Create the new customer
                first_name=new_first,
                last_name=new_last,
                email=new_email,
                phone_number=new_phone,
            )

            if err: # If there was an error creating the customer, show it
                return render(request, "rentals/create_rental.html", {
                    "customers": customers,
                    "instruments": instruments,
                    "error": err,
                })

        # Still no customer? error.
        if not customer_id:
            return render(request, "rentals/create_rental.html", {
                "customers": customers,
                "instruments": instruments,
                "error": "Please select or create a customer."
            })

        if not cart: # No instruments in cart? error.
            return render(request, "rentals/create_rental.html", {
                "customers": customers,
                "instruments": instruments,
                "error": "You must add at least one instrument."
            })

        # All good: create the rental + items
        services.create_rental_with_items(int(customer_id), cart)

        # Clear the cart
        request.session["rental_cart"] = []

        return redirect("rental_list") # Redirect to rental list after successful creation

    # GET: show form
    return render(request, "rentals/create_rental.html", {
        "instruments": instruments,
        "customers": customers,
    })



# ---------------------------------------------------------
# CART OPERATIONS
# ---------------------------------------------------------
# this function adds an instrument to the rental cart
def add_rental_cart(request, instrument_id):
    cart = request.session.get("rental_cart", [])

    if instrument_id not in cart:
        cart.append(instrument_id)

    request.session["rental_cart"] = cart

    rental_mode = request.GET.get("rental_mode", "0")
    return redirect("/instruments/?rental_mode=1")

# this function removes an instrument from the rental cart
def remove_rental_cart(request, instrument_id):
    cart = request.session.get("rental_cart", [])

    if instrument_id in cart:
        cart.remove(instrument_id)

    request.session["rental_cart"] = cart
    return redirect("create_rental")