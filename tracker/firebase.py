"""
Firebase Firestore init and CRUD helpers for DNN topics.
"""
import os
from django.conf import settings

_db = None
_client = None
COLLECTION = "dnn_topics"
STREAK_COLLECTION = "revision_streak"


def _get_client():
    global _client
    if _client is not None:
        return _client
    creds = getattr(settings, "FIREBASE_CREDENTIALS", None)
    if not creds:
        return None
    import firebase_admin
    from firebase_admin import credentials
    try:
        firebase_admin.get_app()
    except ValueError:
        firebase_admin.initialize_app(credentials.Certificate(creds))
    _client = firebase_admin.firestore.client()
    return _client


def get_db():
    global _db
    if _db is None:
        client = _get_client()
        _db = client if client else None
    return _db


def _topic_doc_id(topic_name):
    """Stable document ID from topic name (slug-like)."""
    return topic_name.lower().replace(" ", "_").replace("&", "and").replace("/", "_")


def get_all_topics():
    """Return list of topic dicts from Firestore."""
    db = get_db()
    if not db:
        return []
    coll = db.collection(COLLECTION)
    docs = coll.stream()
    out = []
    for doc in docs:
        d = doc.to_dict()
        d["id"] = doc.id
        out.append(d)
    return sorted(out, key=lambda x: (x.get("order", 999), x.get("topic_name", "")))


def get_topic(topic_id):
    """Get single topic by document id."""
    db = get_db()
    if not db:
        return None
    doc = db.collection(COLLECTION).document(topic_id).get()
    if not doc.exists:
        return None
    d = doc.to_dict()
    d["id"] = doc.id
    return d


def update_topic(topic_id, completed_subtopics=None, notes=None, difficulty=None, last_studied=None):
    """Update topic fields. Pass only fields to update."""
    db = get_db()
    if not db:
        return False
    ref = db.collection(COLLECTION).document(topic_id)
    updates = {}
    if completed_subtopics is not None:
        updates["completed_subtopics"] = completed_subtopics
    if notes is not None:
        updates["notes"] = notes
    if difficulty is not None:
        updates["difficulty"] = difficulty
    if last_studied is not None:
        updates["last_studied"] = last_studied
    if not updates:
        return True
    ref.update(updates)
    return True


def toggle_subtopic(topic_id, subtopic_index, completed):
    """Set one subtopic completed or not by index."""
    topic = get_topic(topic_id)
    if not topic:
        return False
    completed_list = list(topic.get("completed_subtopics") or [])
    n = len(topic.get("subtopics") or [])
    if subtopic_index < 0 or subtopic_index >= n:
        return False
    if completed and subtopic_index not in completed_list:
        completed_list.append(subtopic_index)
        completed_list.sort()
    elif not completed and subtopic_index in completed_list:
        completed_list = [i for i in completed_list if i != subtopic_index]
    return update_topic(topic_id, completed_subtopics=completed_list)


def get_streak():
    """Get current streak: { last_date: ISO date string, streak_days: int }."""
    db = get_db()
    if not db:
        return {"last_date": None, "streak_days": 0}
    doc = db.collection(STREAK_COLLECTION).document("current").get()
    if not doc.exists:
        return {"last_date": None, "streak_days": 0}
    d = doc.to_dict()
    return {
        "last_date": d.get("last_date"),
        "streak_days": d.get("streak_days", 0),
    }


def record_study_date(date_iso):
    """Record that user studied on date_iso; updates streak."""
    db = get_db()
    if not db:
        return 0
    from datetime import datetime, timedelta
    ref = db.collection(STREAK_COLLECTION).document("current")
    doc = ref.get()
    today = date_iso  # e.g. "2025-02-26"
    if not doc.exists:
        ref.set({"last_date": today, "streak_days": 1})
        return 1
    d = doc.to_dict()
    last = d.get("last_date") or ""
    streak = d.get("streak_days", 0)
    try:
        last_dt = datetime.strptime(last, "%Y-%m-%d").date()
        cur_dt = datetime.strptime(today, "%Y-%m-%d").date()
    except ValueError:
        ref.set({"last_date": today, "streak_days": 1})
        return 1
    if cur_dt == last_dt:
        return streak  # already recorded today
    if cur_dt - last_dt == timedelta(days=1):
        streak += 1
    else:
        streak = 1
    ref.set({"last_date": today, "streak_days": streak})
    return streak


def seed_topics(topics_data):
    """
    Seed Firestore with topics. topics_data is list of dicts with
    topic_name, subtopics. Creates or overwrites docs by stable id.
    """
    db = get_db()
    if not db:
        raise RuntimeError("Firebase not configured")
    coll = db.collection(COLLECTION)
    for order, item in enumerate(topics_data):
        topic_name = item["topic_name"]
        subtopics = item.get("subtopics", [])
        doc_id = _topic_doc_id(topic_name)
        coll.document(doc_id).set({
            "topic_name": topic_name,
            "subtopics": subtopics,
            "completed_subtopics": [],
            "notes": "",
            "last_studied": None,
            "difficulty": "",
            "order": order,
        }, merge=True)
    return len(topics_data)
