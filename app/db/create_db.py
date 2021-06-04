import sqlite3
import os

# Current file path
this_path = os.path.dirname(os.path.abspath(__file__))

# DB connection
con = sqlite3.connect(f'{this_path}/grocery.db')
cur = con.cursor()

# Create table
cur.execute('''CREATE TABLE IF NOT EXISTS item
               (id INTEGER PRIMARY KEY AUTOINCREMENT, name varchar(255), description varchar(255), price REAL, is_offer BOOLEAN NOT NULL CHECK (is_offer IN (0, 1)))''')

# Save changes
con.commit()

# close connection
con.close()
