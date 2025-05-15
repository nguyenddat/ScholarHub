import time
import threading

from database.init_db import get_db
from models import Profile

class ProfileManager:
    def __init__(self, time_limit: int = 3600):
        self.profiles = []
        self.last_request_time = []

        self.time_limit = time_limit
        self.lock = threading.Lock()

        self.monitor_thread = threading.Thread(target=self._monitor, daemon=True)
        self.monitor_thread.start()

        self.wait_for_update = False

    def _monitor(self):
        while True:
            time.sleep(3)
            with self.lock:
                if self.wait_for_update:
                    expired_users = [user_id for user_id, last_time in zip(self.profiles, self.last_request_time)
                                     if time.time() - last_time >= self.time_limit]

                    for user_id in expired_users:
                        print(f"[Profile Monitor] Re-ingesting profile for user: {user_id}")
                        try:
                            self.re_ingest(user_id)
                            print(f"[Profile Monitor] Done re-ingesting profile for user: {user_id}]")
                        except Exception as e:
                            print(f"[Profile Monitor] Failed to re-ingest user {user_id}: {str(e)}")

    def record_request(self, user_id):
        self.wait_for_update = True
        with self.lock:
            if user_id not in self.profiles:
                self.profiles.append(user_id)
                self.last_request_time.append(time.time())
            
            else:
                index = self.profiles.index(user_id)
                self.last_request_time[index] = time.time()

    def re_ingest(self, user_id):
        db = next(get_db())
        
        Profile.update_criteria(db, user_id)
        index = self.profiles.index(user_id)
        del self.profiles[index]
        del self.last_request_time[index]

        if len(self.profiles) == 0:
            self.wait_for_update = False

    def re_evaluate(self, db, user_id):
        Profile.update_criteria(db, user_id)

        if user_id in self.profiles:
            index = self.profiles.index(user_id)
            del self.profiles[index]
            del self.last_request_time[index]

            if len(self.profiles) == 0:
                self.wait_for_update = False

profile_manager = ProfileManager()