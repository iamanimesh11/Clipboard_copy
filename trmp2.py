import os
from datetime import datetime
import firebase_admin
from firebase_admin import credentials, firestore

# -------------------------
# Firebase Initialization
AIRFLOW_HOME = os.getenv("AIRFLOW_HOME", "/opt/airflow")
CREDENTIALS_PATH = os.path.join(AIRFLOW_HOME, "common", "credentials")
cred = credentials.Certificate(os.path.join(CREDENTIALS_PATH, "firebase_cred.json"))
firebase_admin.initialize_app(cred)
db = firestore.client()
API_TRACK_COLLECTION = "api_usage"

# -------------------------
# Utility Functions

def get_today_key():
    return datetime.utcnow().strftime("%Y-%m-%d")

def get_status(api_name):
    key = get_today_key()
    doc = db.collection(API_TRACK_COLLECTION).document(key).get()
    if doc.exists:
        data = doc.to_dict().get(api_name, {})
        return {
            "count": data.get("count", 0),
            "failures": data.get("failures", 0),
            "is_down": data.get("is_down", False)
        }
    return {"count": 0, "failures": 0, "is_down": False}

def increment_api_count(api_name):
    key = get_today_key()
    doc_ref = db.collection(API_TRACK_COLLECTION).document(key)
    doc_ref.set({f"{api_name}.count": firestore.Increment(1)}, merge=True)

def increment_failure(api_name):
    key = get_today_key()
    doc_ref = db.collection(API_TRACK_COLLECTION).document(key)
    doc_ref.set({f"{api_name}.failures": firestore.Increment(1)}, merge=True)

def reset_failure_count(api_name):
    key = get_today_key()
    doc_ref = db.collection(API_TRACK_COLLECTION).document(key)
    doc_ref.set({f"{api_name}.failures": 0}, merge=True)

def mark_api_status(api_name, is_down):
    key = get_today_key()
    doc_ref = db.collection(API_TRACK_COLLECTION).document(key)
    doc_ref.set({f"{api_name}.is_down": is_down}, merge=True)

def should_block_api(api_name, max_limit=2500, max_failures=5):
    status = get_status(api_name)
    return status["count"] >= max_limit or status["failures"] >= max_failures

def print_api_status(api_name):
    status = get_status(api_name)
    print(f"[{api_name.upper()}] Count: {status['count']}, Failures: {status['failures']}, Is Down: {status['is_down']']}")




from api_tracker import *

api_name = "tomtom"

if should_block_api(api_name):
    mark_api_status(api_name, True)
    print("API is currently blocked due to limit or failures.")
else:
    try:
        # Your actual API call here
        response = requests.get("https://...")
        response.raise_for_status()

        increment_api_count(api_name)
        reset_failure_count(api_name)
        mark_api_status(api_name, False)

    except Exception as e:
        increment_failure(api_name)
        print("API call failed.")
