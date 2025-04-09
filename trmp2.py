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


# -----------------------------
# Set up paths
AIRFLOW_HOME = os.getenv("AIRFLOW_HOME", "/opt/airflow")
if AIRFLOW_HOME != "/opt/airflow":
    BASE_DIR = os.path.abspath(os.path.join(AIRFLOW_HOME, "..",".."))
    AIRFLOW_HOME = BASE_DIR

CREDENTIALS_PATH = os.path.join(AIRFLOW_HOME, "common", "credentials")

COMMON_PATH = os.path.join(AIRFLOW_HOME, "common", "logging_and_monitoring")
sys.path.append(COMMON_PATH)

LOGS_PATH = os.path.join(COMMON_PATH, "logs")
sys.path.append(LOGS_PATH)
print(AIRFLOW_HOME)


# Firebase setup
cred = credentials.Certificate(os.path.join(CREDENTIALS_PATH, "firebase_cred.json"))
firebase_admin.initialize_app(cred)
db = firestore.client()
API_TRACK_COLLECTION = "api_usage"

# -----------------------------
# Logging setup
# from centralized_logging import setup_logger

# script_logs_path = os.path.join(LOGS_PATH, "db_utils.log")
# logger = setup_logger("Road_Data_ETL", "db_utils", "python", script_logs_path)

# -----------------------------
# Utility functions
def get_today_key():
    return datetime.utcnow().strftime("%Y-%m-%d")

def get_api_count():
    key = get_today_key()
    doc_ref = db.collection(API_TRACK_COLLECTION).document(key)
    doc = doc_ref.get()
    if doc.exists:
        return doc.to_dict().get("count", 0)
    return 0

def increment_api_count():
    key = get_today_key()
    doc_ref = db.collection(API_TRACK_COLLECTION).document(key)
    doc_ref.set({"count": firestore.Increment(1)}, merge=True)

# -----------------------------
# Main logic
MAX_DAILY_LIMIT = 2500
current_count = get_api_count()

if current_count >= MAX_DAILY_LIMIT:
    print("API limit reached")
    print("API daily usage limit reached.")
else:
    increment_api_count()
    print(f"API call allowed. Current count: {current_count + 1}")
