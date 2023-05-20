from firebase_admin import firestore
from typing import List

doc_path = "line/talk"
def get_message_list()->List[str]:
    db = firestore.client()
    talk = db.document(doc_path).get().to_dict()
    if talk is None:
        return []
    else:
        return talk["message_list"]

def set_message_list(lst:list):
    db = firestore.client()
    db.document(doc_path).set({
        "message_list":lst
    })

def reset_message_list():
    db = firestore.client()
    db.document(doc_path).set({
        "message_list":[]
    })