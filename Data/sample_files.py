from django.db import connection

def load_samples():
    """
    Inserts sample instruments, customers, and rentals into SQLite.
    """

    with connection.cursor() as cursor:

        print("Loading sample instrument data...")
        cursor.execute("""
            INSERT INTO instrument (barcode, name, category, status, color)
            VALUES
               ('0001', 'Yamaha Trumpet', 'Brass', 'available', 'Gold'),
               ('0002', 'Selmer Clarinet', 'Woodwind', 'available', 'Black'),
               ('0003', 'Pearl Snare Drum', 'Percussion', 'rented', 'Silver'),
               ('0004', 'Fender Violin', 'Strings', 'available', 'Brown')
            ;
        """)

        print("Loading sample customer data...")
        cursor.execute("""
            INSERT INTO customer (first_name, last_name, email, phone_number)
            VALUES
               ('John', 'Doe', 'john@example.com', '555-1234'),
               ('Jane', 'Smith', 'jane@example.com', '555-5678'),
               ('Emily', 'Johnson', 'emily@example.com', '555-8765')
            ;
        """)


        print("Loading sample rental data...")

        cursor.execute("""
            INSERT INTO rental (customer_id, rental_date, returned, return_date)
            VALUES
                (1, datetime('now', '-10 days'), 0, NULL),
                (2, datetime('now', '-20 days'), 1, datetime('now', '-5 days'));
        """)

        # Insert rental items
        cursor.execute("""
            INSERT INTO rentalitem (rental_id, instrument_id)
            VALUES
                (1, 1),   -- rental 1 includes instrument 1
                (1, 3),   -- rental 1 also includes instrument 3
                (2, 2);   -- rental 2 includes instrument 2
        """)

    print("Sample data loaded successfully!")

    
