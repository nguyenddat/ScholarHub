import time
import threading

from database.init_db import get_db
from models import Profile

class ProfileManager:
    def __init__(self, time_limit: int = 3600):
        self.profile_last_time = {}  # {user_id: last_request_time}
        self.time_limit = time_limit
        self.lock = threading.Lock()

        self.monitor_thread = threading.Thread(target=self._monitor, daemon=True)
        self.monitor_thread.start()

    def _monitor(self):
        while True:
            time.sleep(30)
            now = time.time()

            with self.lock:
                expired_users = [uid for uid, ts in self.profile_last_time.items()
                                 if now - ts >= self.time_limit]

            for user_id in expired_users:
                print(f"[Profile Monitor] Re-ingesting profile for user: {user_id}")
                try:
                    self.re_ingest(user_id)
                    print(f"[Profile Monitor] Done re-ingesting profile for user: {user_id}")
                except Exception as e:
                    print(f"[Profile Monitor] Failed to re-ingest user {user_id}: {e}")

    def record_request(self, user_id):
        with self.lock:
            self.profile_last_time[user_id] = time.time()

    def re_ingest(self, user_id):
        with self.lock:
            if user_id not in self.profile_last_time:
                return

        try:
            db = next(get_db())
            Profile.update_criteria(db, user_id)
        finally:
            db.close()

        # Xóa user_id sau khi xử lý xong
        with self.lock:
            self.profile_last_time.pop(user_id, None)

    def re_evaluate(self, db, user_id):
        Profile.update_criteria(db, user_id)

        with self.lock:
            self.profile_last_time.pop(user_id, None)

profile_manager = ProfileManager()