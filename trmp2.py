import os
from datetime import datetime
import firebase_admin
from firebase_admin import credentials, firestore

class ApiMonitor:
    def __init__(self, cred_path, collection="api_usage"):
        if not firebase_admin._apps:
            cred = credentials.Certificate(cred_path)
            firebase_admin.initialize_app(cred)

        self.db = firestore.client()
        self.collection = collection

    def _get_today_key(self):
        return datetime.utcnow().strftime("%Y-%m-%d")

    def get_status(self, api_name):
        key = self._get_today_key()
        doc = self.db.collection(self.collection).document(key).get()
        if doc.exists:
            data = doc.to_dict().get(api_name, {})
            return data.get("count", 0), data.get("failures", 0), data.get("is_down", False)
        return 0, 0, False

    def increment_api_count(self, api_name):
        key = self._get_today_key()
        self.db.collection(self.collection).document(key).set(
            {f"{api_name}.count": firestore.Increment(1)}, merge=True
        )

    def increment_failure(self, api_name):
        key = self._get_today_key()
        self.db.collection(self.collection).document(key).set(
            {f"{api_name}.failures": firestore.Increment(1)}, merge=True
        )

    def reset_failure_count(self, api_name):
        key = self._get_today_key()
        self.db.collection(self.collection).document(key).set(
            {f"{api_name}.failures": 0}, merge=True
        )

    def mark_api_status(self, api_name, is_down):
        key = self._get_today_key()
        self.db.collection(self.collection).document(key).set(
            {f"{api_name}.is_down": is_down}, merge=True
        )
