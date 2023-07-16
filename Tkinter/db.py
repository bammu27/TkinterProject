import sqlite3
import pytest

class Database:
    def __init__(self, db):
        self.conn = sqlite3.connect(db)
        self.curr = self.conn.cursor()
        self.curr.execute("CREATE TABLE IF NOT EXISTS parts (id INTEGER PRIMARY KEY AUTOINCREMENT, part text, customer text, retailer text, price INTEGER,quantity INTEGER)")
        self.conn.commit()

    def fetch(self):
        self.curr.execute("SELECT * FROM parts")
        rows = self.curr.fetchall()
        return rows

    def insert(self, part, customer, retailer, price, quantity):
        self.curr.execute("INSERT INTO parts(part, customer, retailer, price, quantity) VALUES (?,?,?,?,?)", (part, customer, retailer, price, quantity))
        self.conn.commit()

    def remove(self, id):
        self.curr.execute("DELETE FROM parts WHERE id=?", (id,))
        self.conn.commit()

    def update(self, id, part, customer, retailer, price, quantity):
        self.curr.execute("UPDATE parts SET part=?, customer=?, retailer=?, price=?, quantity=? WHERE id=?", (part, customer, retailer, price, quantity, id))
        self.conn.commit()

    def _del_(self):
        self.conn.close()


# Create an instance of the Database class
db = Database("store1.db")

# Insert 6 rows into the table
#db.insert(1, "Engine Oil", "John Smith", "AutoZone", 30)
#db.insert(2, "Brake Pads", "Sarah Johnson", "Advance Auto Parts", 40)
#db.insert(4, "Air Filter", "Emily Anderson", "NAPA Auto Parts", 20)
#db.insert(5, "Battery", "Daniel Wilson", "Pep Boys", 100)
#db.insert(6, "Tire", "Jessica Thompson", "Discount Tire", 150)
# Close the database connection
