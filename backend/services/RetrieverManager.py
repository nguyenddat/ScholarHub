import time
import threading

from ai.SmartSearch.v1.Retriever import retriever

class RetrieverManager:
    def __init__(self, request_limit: int = 30, time_limit: int = 30):
        self.retriever = retriever

        self.wait_for_ingest = False
        self.request_count = 0
        self.last_request_time = time.time()
        self.request_limit = request_limit
        self.time_limit = time_limit
        self.lock = threading.Lock()

        self.monitor_thread = threading.Thread(target=self._monitor, daemon=True)
        self.monitor_thread.start()

    def _monitor(self):
        while True:
            time.sleep(3)
            with self.lock:
                elapsed = time.time() - self.last_request_time
                
                if (self.wait_for_ingest) and ((elapsed > self.time_limit) or (self.request_count >= self.request_limit)):
                    print("[Monitor] Re-ingesting vector store...")
                    self.re_ingest()

    def record_request(self):
        self.wait_for_ingest = True
        with self.lock:
            self.request_count += 1
            self.last_request_time = time.time()

    def re_ingest(self):
        self.retriever.re_ingest()

        self.wait_for_ingest = False
        self.request_count = 0
        self.last_request_time = time.time()
    
retriever_manager = RetrieverManager()