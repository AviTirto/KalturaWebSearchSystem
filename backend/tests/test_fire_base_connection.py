import firebase_admin
from firebase_admin import credentials, firestore

cred = credentials.Certificate("../firebase_key.json")
firebase_admin.initialize_app(cred)

db = firestore.client()

# Define data to add
lect_data = {
    "title": "test",
    "embed_link": "test",
    "date": "test"
}

# Add document with custom key
db.collection("lectures").document(f"{str(122445)}").set(lect_data)