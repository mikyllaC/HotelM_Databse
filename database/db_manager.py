import sqlite3

# Connect to the database
conn = sqlite3.connect(r"C:\Users\User\Desktop\Hotel Management Database\database\Hotel_Management.db")
cursor = conn.cursor()

# SQL insert statement to Employee informations
sql = 'INSERT INTO EMPLOYEE (LAST_NAME, FIRST_NAME, POSITION) VALUES ("Samuel", "Muralid", "CEO");'
sql = 'INSERT INTO EMPLOYEE (LAST_NAME, FIRST_NAME, POSITION) VALUES ("Karla", "Castro", "Manager");'

cursor.executemany('''INSERT INTO EMPLOYEE (LAST_NAME, FIRST_NAME, POSITION) VALUES (?, ?, ?)'''sql)


cursor.execute(sql)

# Commit the transaction
conn.commit()

# Close the connection
conn.close()
