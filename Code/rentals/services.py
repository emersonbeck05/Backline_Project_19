# rentals/services.py
from django.db import connection, IntegrityError


# ---------------------------------
# Instruments
# ---------------------------------
# this function retrieves all instruments from the database
def get_all_instruments():
    """
    Return all instruments as a list of dicts.
    Used by the instrument list page.
    """
    with connection.cursor() as cursor: # Open a database cursor
        cursor.execute(""" 
            SELECT id, barcode, name, category, status, color
            FROM instrument
            ORDER BY name ASC;
        """)
        # Fetch all rows from the executed query
        rows = cursor.fetchall() # Each row is a tuple

    instruments = [] # Initialize an empty list to hold instrument dicts
    for row in rows: # Iterate over each row
        instruments.append({
            "id": row[0],
            "barcode": row[1],
            "name": row[2],
            "category": row[3],
            "status": row[4],
            "color": row[5],
        }) # Append a dict representing the instrument to the list
    return instruments # Return the list of instrument dicts

#this function adds a new instrument to the database
def add_instrument(barcode, name, category, color, status="available"):
    """
    Insert a new instrument. Returns (success, error_message).
    """
    try:
        with connection.cursor() as cursor:
            cursor.execute("""
                INSERT INTO instrument (barcode, name, category, status, color)
                VALUES (%s, %s, %s, %s, %s);
            """, [barcode, name, category, status, color]) # Execute the insert query with provided values
        return True, None
    except IntegrityError:
        return False, "An instrument with that barcode already exists."

#this function retrieves instruments based on a list of IDs
def get_instruments_for_ids(id_list):
    """
    Given a list of instrument IDs (from the cart), return a list of dicts.
    """
    if not id_list:
        return []

    placeholders = ", ".join(["%s"] * len(id_list))
    query = f"""
        SELECT id, name, barcode, color, status
        FROM instrument
        WHERE id IN ({placeholders});
    """

    with connection.cursor() as cursor:
        cursor.execute(query, id_list)
        rows = cursor.fetchall()

    instruments = []
    for row in rows:
        instruments.append({
            "id": row[0],
            "name": row[1],
            "barcode": row[2],
            "color": row[3],
            "status": row[4],
        })
    return instruments

#this function updates the status of a specific instrument
def update_instrument_status(instrument_id, new_status):
    """
    Update status for a single instrument.
    """
    with connection.cursor() as cursor:
        cursor.execute("""
            UPDATE instrument SET status = %s WHERE id = %s;
        """, [new_status, instrument_id])# These lines update the instrument's status in the database


# ---------------------------------
# Customers
# ---------------------------------
#this function returns minimal customer data for dropdown menus
def get_customers_dropdown():
    """
    Return minimal data for the customer dropdown on the rental screen.
    Each row is (id, first_name, last_name).
    """
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT id, first_name, last_name
            FROM customer
            ORDER BY last_name, first_name;
        """)
        return cursor.fetchall()

#this function creates a new customer in the database
def create_customer(first_name, last_name, email, phone_number):
    """
    Create a new customer. Returns (customer_id, error_message).
    If the email already exists, returns (None, error).
    """
    try:
        with connection.cursor() as cursor:
            cursor.execute("""
                INSERT INTO customer (first_name, last_name, email, phone_number)
                VALUES (%s, %s, %s, %s);
            """, [first_name, last_name, email, phone_number])
            customer_id = cursor.lastrowid
        return customer_id, None
    except IntegrityError:
        return None, "A customer with that email already exists."


# ---------------------------------
# Rentals
# ---------------------------------
#this function creates a rental and associated rental items
def create_rental_with_items(customer_id, instrument_ids):
    """
    Create a rental row and one rentalitem row per instrument.
    Also sets each instrument status to 'rented'.

    Returns the new rental_id.
    """
    if not instrument_ids:
        raise ValueError("No instruments supplied to create_rental_with_items().")

    with connection.cursor() as cursor:
        # Create the rental header
        cursor.execute("""
            INSERT INTO rental (customer_id, rental_date, returned)
            VALUES (%s, datetime('now'), 0);
        """, [customer_id])
        rental_id = cursor.lastrowid

        # Create rental_item rows and update instrument statuses
        for inst_id in instrument_ids:
            cursor.execute("""
                INSERT INTO rentalitem (rental_id, instrument_id)
                VALUES (%s, %s);
            """, [rental_id, inst_id])

            cursor.execute("""
                UPDATE instrument SET status = 'rented'
                WHERE id = %s;
            """, [inst_id])

    return rental_id

#this function processes the return of a full rental
def return_full_rental(rental_id):
    with connection.cursor() as cursor:

        # Get all instruments in this rental
        cursor.execute("""
            SELECT instrument_id FROM rentalitem
            WHERE rental_id = %s;
        """, [rental_id])
        items = cursor.fetchall()

        # Set instruments to available
        for (instrument_id,) in items:
            cursor.execute("""
                UPDATE instrument SET status = 'available'
                WHERE id = %s;
            """, [instrument_id])

        # Mark rental returned
        cursor.execute("""
            UPDATE rental
            SET returned = 1,
                return_date = datetime('now')
            WHERE id = %s;
        """, [rental_id])

    connection.commit()
