import face_recognition
import cv2
import sqlite3
import numpy as np
import datetime

# Connect to SQLite DB
conn = sqlite3.connect('face_recognition.db')
cursor = conn.cursor()

# Create recognition_logs table if it doesn't exist
cursor.execute('''
CREATE TABLE IF NOT EXISTS recognition_logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    recognized_at TEXT NOT NULL
)
''')
conn.commit()

# Load encodings and names from DB
cursor.execute("SELECT name, encoding FROM registrations")
rows = cursor.fetchall()

known_names = []
known_encodings = []

for name, encoding_blob in rows:
    known_names.append(name)
    # Convert BLOB back to numpy array
    encoding = np.frombuffer(encoding_blob, dtype=np.float64)
    known_encodings.append(encoding)

print(f"Loaded {len(known_names)} known faces from database.")
    
cap = cv2.VideoCapture(0)

print("Recognizing... Press 'q' to quit.")

while True:
    ret, frame = cap.read()
    if not ret:
        break

    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    face_locations = face_recognition.face_locations(rgb)
    face_encodings = face_recognition.face_encodings(rgb, face_locations)

    for face_encoding, face_location in zip(face_encodings, face_locations):
        matches = face_recognition.compare_faces(known_encodings, face_encoding)
        name = "Unknown"

        if True in matches:
            matched_idx = matches.index(True)
            name = known_names[matched_idx]

            # Draw box and label on frame
            top, right, bottom, left = face_location
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
            cv2.putText(frame, name, (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)

            # Insert recognition log into DB
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            cursor.execute(
                "INSERT INTO recognition_logs (name, recognized_at) VALUES (?, ?)",
                (name, timestamp)
            )
            conn.commit()

            print(f"{name} recognized at {timestamp}")

    cv2.imshow("Recognize Face", frame)
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
conn.close()
