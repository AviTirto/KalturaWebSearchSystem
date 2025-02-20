import firebase_admin
from firebase_admin import credentials, firestore
import os
import sys

# Adjust path for project root
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
print("PROJECT ROOT: ", project_root)
sys.path.insert(0, project_root)

from backend.db.models import Lecture, Subtitle

def get_db():
    # Use the project_root that's already defined at the top of the file
    firebase_key_path = os.getenv('FIREBASE_KEY_PATH', os.path.join(project_root, "backend/firebase_key.json"))
    cred = credentials.Certificate(firebase_key_path)
    firebase_admin.initialize_app(cred)
    db = firestore.client()
    return db

def add_lecture(db, lecture: Lecture):

    lecture_dict = lecture.model_dump()
    del lecture_dict["lecture_id"]

    db.collection("lectures").document(lecture.get_lecture_id_as_str()).set(lecture_dict)

def add_subtitles(db, subtitles: Subtitle):
    subtitle_dict = subtitles.model_dump()
    del subtitle_dict["chunk_id"]

    db.collection("subtitles").document(subtitles.get_chunk_id_as_str()).set(subtitle_dict)

def add_lectures_batch(db, lectures: list[Lecture]):
    batch = db.batch()
    
    for lecture in lectures:
        lecture_dict = lecture.model_dump()
        del lecture_dict["lecture_id"]
        doc_ref = db.collection("lectures").document(lecture.get_lecture_id_as_str())
        batch.set(doc_ref, lecture_dict)
    
    batch.commit()

def add_subtitles_batch(db, subtitles_list: list[Subtitle]):
    batch = db.batch()
    
    for subtitles in subtitles_list:
        subtitle_dict = subtitles.model_dump()
        del subtitle_dict["chunk_id"]
        doc_ref = db.collection("subtitles").document(subtitles.get_chunk_id_as_str())
        batch.set(doc_ref, subtitle_dict)
    
    batch.commit()

async def get_lecture_batch(db, lecture_ids_list: list[int]):
    lecture_refs = [db.collection("lectures").document(str(id)) for id in lecture_ids_list]
    
    # Get all documents in a single request
    docs = db.get_all(lecture_refs)
    
    # Create a dictionary mapping lecture_id to its data
    result = {}

    for doc in docs:
        if doc.exists:
            lecture_id = int(doc.id)
            result[lecture_id] = doc.to_dict()
    
    return result

def get_subtitle_metadata_batch(db, clip_ids_list: list[int]):
    # Convert IDs to strings
    lecture_refs = [db.collection("subtitles").document(str(id)) for id in clip_ids_list]

    # Get all documents in a single request
    docs = db.get_all(lecture_refs)
    
    # Create a dictionary mapping lecture_id to its data
    result = {}

    for doc in docs:
        if doc.exists:
            lecture_id = int(doc.id)
            result[lecture_id] = doc.to_dict()
    
    return result

def add_slides_batch(db, slides: list[Slide]):
    batch = db.batch()

    for slide in slides:
        slide_dict = slide.model_dump()
        del slide_dict["slide_id"]
        doc_ref = db.collection("slides").document(slide.get_slide_id_as_str())
        batch.set(doc_ref, slide_dict)
    
    batch.commit()
            
    