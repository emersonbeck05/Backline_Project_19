import sqlite3

db_path = "inventory.db"

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

print("Rebuilding database...")

cursor.execute("""
CREATE TABLE IF NOT EXISTS instrument (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    barcode TEXT UNIQUE NOT NULL,
    name TEXT NOT NULL,
    category TEXT NOT NULL,
    status TEXT NOT NULL DEFAULT 'available',
    color TEXT
);
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS customer (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    phone_number TEXT
);
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS rental (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    customer_id INTEGER NOT NULL,
    rental_date TEXT NOT NULL,
    returned INTEGER NOT NULL DEFAULT 0,
    return_date TEXT,
    FOREIGN KEY(customer_id) REFERENCES customer(id)
);
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS rental_item (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    rental_id INTEGER NOT NULL,
    instrument_id INTEGER NOT NULL,
    FOREIGN KEY(rental_id) REFERENCES rental(id),
    FOREIGN KEY(instrument_id) REFERENCES instrument(id)
);
""")

conn.commit()
conn.close()

print("Database initialized successfully!")
