import face_recognition
import cv2
import sqlite3
import numpy as np
import os
import datetime

# Connect to SQLite DB (creates if not exists)
conn = sqlite3.connect('face_recognition.db')
cursor = conn.cursor()

# Create table if not exists
cursor.execute('''
CREATE TABLE IF NOT EXISTS registrations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    encoding BLOB NOT NULL,
    registration_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
''')
conn.commit()

name = input("Enter your name: ")

cap = cv2.VideoCapture(0)

print("Press 's' to capture your face")

while True:
    ret, frame = cap.read()
    if not ret:
        break

    cv2.imshow("Register Face", frame)
    key = cv2.waitKey(1)

    if key == ord('s'):
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        face_locations = face_recognition.face_locations(rgb)

        if face_locations:
            face_encoding = face_recognition.face_encodings(rgb, face_locations)[0]

            # Convert encoding (numpy array) to bytes for SQLite storage
            encoding_bytes = face_encoding.tobytes()

            # Insert into DB
            cursor.execute(
                "INSERT INTO registrations (name, encoding, registration_time) VALUES (?, ?, ?)",
                (name, encoding_bytes, datetime.datetime.now())
            )
            conn.commit()

            print(f"Face captured and saved for {name}")
            break
        else:
            print("No face detected, try again.")

cap.release()
cv2.destroyAllWindows()
conn.close()
