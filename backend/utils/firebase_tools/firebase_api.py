import firebase_admin
from firebase_admin import credentials, firestore
import os
import sys

# Adjust path for project root
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../.."))
sys.path.insert(0, project_root)

from backend.db.models import Lecture, Subtitles

def get_db():
    cred = credentials.Certificate("../../firebase_key.json")
    firebase_admin.initialize_app(cred)
    db = firestore.client()
    return db

def add_lecture(db, lecture: Lecture):

    lecture_dict = lecture.model_dump()
    del lecture_dict["lecture_id"]

    db.collection("lectures").document(lecture.get_lecture_id_as_str()).set(lecture_dict)

def add_subtitles(db, subtitles: Subtitles):
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

def add_subtitles_batch(db, subtitles_list: list[Subtitles]):
    batch = db.batch()
    
    for subtitles in subtitles_list:
        subtitle_dict = subtitles.model_dump()
        del subtitle_dict["chunk_id"]
        doc_ref = db.collection("subtitles").document(subtitles.get_chunk_id_as_str())
        batch.set(doc_ref, subtitle_dict)
    
    batch.commit()
    
    