import sqlite3

# Connect to the database
conn = sqlite3.connect(r"C:\Users\User\Desktop\Hotel Management Database\database\Hotel_Management.db")
cursor = conn.cursor()

# Data to insert
employees = [
    ("Samuel", "Muralid", "CEO"),
    ("Karla", "Castro", "Manager")
]

# Use executemany to insert multiple records
cursor.executemany('''
    INSERT INTO EMPLOYEE (LAST_NAME, FIRST_NAME, POSITION) VALUES (?, ?, ?)
''', employees)

# Commit the transaction
conn.commit()

# Close the connection
conn.close()
