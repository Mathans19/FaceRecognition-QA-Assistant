import sqlite3

# Connect to (or create) the database file in your project folder
conn = sqlite3.connect('face_recognition.db')

# Create a cursor object to execute SQL commands
cursor = conn.cursor()

# Create the registrations table
cursor.execute('''
CREATE TABLE IF NOT EXISTS registrations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    encoding BLOB NOT NULL,
    registration_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
''')

# Commit changes and close connection
conn.commit()
conn.close()

print("Database and table created successfully.")
