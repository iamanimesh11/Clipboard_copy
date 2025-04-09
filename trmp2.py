def mark_api_status(api_name, is_down):
    key = get_today_key()
    doc_ref = db.collection(API_TRACK_COLLECTION).document(key)
    doc_ref.set({f"{api_name}.is_down": is_down}, merge=True)

def increment_failure(api_name):
    key = get_today_key()
    doc_ref = db.collection(API_TRACK_COLLECTION).document(key)
    doc_ref.set({f"{api_name}.failures": firestore.Increment(1)}, merge=True)

def reset_failure_count(api_name):
    key = get_today_key()
    doc_ref = db.collection(API_TRACK_COLLECTION).document(key)
    doc_ref.set({f"{api_name}.failures": 0}, merge=True)

def get_status(api_name):
    key = get_today_key()
    doc = db.collection(API_TRACK_COLLECTION).document(key).get()
    if doc.exists:
        data = doc.to_dict().get(api_name, {})
        return data.get("count", 0), data.get("failures", 0), data.get("is_down", False)
    return 0, 0, False
