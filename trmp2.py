import requests
import sys
import os
import random
import psycopg2
from psycopg2 import extras
from geopy.distance import geodesic
from datetime import datetime
import firebase_admin
from firebase_admin import credentials, firestore
import logging
# -----------------------------
# Set up paths
AIRFLOW_HOME = os.getenv("AIRFLOW_HOME", "/opt/airflow")
if AIRFLOW_HOME != "/opt/airflow":
    BASE_DIR = os.path.abspath(os.path.join(AIRFLOW_HOME, "..", ".."))
    AIRFLOW_HOME = BASE_DIR

CREDENTIALS_PATH = os.path.join(AIRFLOW_HOME, "common", "credentials")
COMMON_PATH = os.path.join(AIRFLOW_HOME, "common", "logging_and_monitoring")
LOGS_PATH = os.path.join(COMMON_PATH, "logs")

sys.path.append(COMMON_PATH)
sys.path.append(LOGS_PATH)

# -----------------------------
# Firebase setup
cred = credentials.Certificate(os.path.join(CREDENTIALS_PATH, "firebase_cred.json"))
if not firebase_admin._apps:
    firebase_admin.initialize_app(cred)

db = firestore.client()
API_TRACK_COLLECTION = "api_usage"

# -----------------------------
# Logging setup

script_logs_path = os.path.join(LOGS_PATH, "db_utils.log")

# -----------------------------
# Utility functions
def get_today_key():
    return datetime.utcnow().strftime("%Y-%m-%d")

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

def increment_api_count(api_name):
    key = get_today_key()
    doc_ref = db.collection(API_TRACK_COLLECTION).document(key)
    doc_ref.set({f"{api_name}.count": firestore.Increment(1)}, merge=True)

def get_status(api_name):
    key = get_today_key()
    doc = db.collection(API_TRACK_COLLECTION).document(key).get()

    if doc.exists:
        data = doc.to_dict().get(api_name, {})
        logging.info(f"Fetched status for {api_name}: {data}")
        return data.get("count", 0), data.get("failures", 0), data.get("is_down", False)
    else:
        logging.warning(f"No status document found for {api_name}")
        return 0, 0, False

# -----------------------------
# Main logic
MAX_LIMIT = 2500
MAX_FAILURES = 5

count, failures, is_down = get_status("tomtom")
logging.info(f"TomTom - Count: {count}, Failures: {failures}, Is Down: {is_down}")

if count >= MAX_LIMIT or failures >= MAX_FAILURES:
    mark_api_status("tomtom", True)
    mark_api_status("weather", True)
    logging.error("TomTom API is DOWN due to limits or failures")
else:
    try:
        # Replace with actual API endpoint
      
        response = requests.get("...")  
        response.raise_for_status()

        increment_api_count("weather")
        increment_api_count("tomtom")

        reset_failure_count("tomtom")
        reset_failure_count("weather")

        mark_api_status("tomtom", False)
        mark_api_status("weather", False)

        logging.info("API call successful, counts updated, failures reset.")

    except requests.RequestException as e:
        increment_failure("weather")
        increment_failure("tomtom")

        logging.exception("TomTom API request failed")
