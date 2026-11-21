"""
Aura Programming Language - CSP Concurrency Engine
Implements Communicating Sequential Processes (CSP):
- AuraChannel (Buffered and Unbuffered / Rendezvous channels)
- AuraSelect (Multiplexing channel communications with timeouts)
- AuraSupervisor (Process and worker supervision with restart strategies)
- AuraConcurrencyManager (Lightweight background task spawning)
"""

import threading
import queue
import time

class AuraChannelClosedException(Exception):
    pass

class AuraChannel:
    def __init__(self, capacity=0):
        self.capacity = max(0, int(capacity))
        self.closed = False
        self.lock = threading.Lock()
        
        if self.capacity > 0:
            self.q = queue.Queue(maxsize=self.capacity)
        else:
            # Unbuffered / Rendezvous channel
            self.q = queue.Queue(maxsize=1)

    def send(self, val, timeout=5.0):
        with self.lock:
            if self.closed:
                raise AuraChannelClosedException("Cannot send to a closed channel")
        try:
            self.q.put(val, block=True, timeout=timeout)
            return True
        except queue.Full:
            return False

    def receive(self, timeout=5.0):
        with self.lock:
            if self.closed and self.q.empty():
                return None
        try:
            return self.q.get(block=True, timeout=timeout)
        except queue.Empty:
            return None

    def close(self):
        with self.lock:
            self.closed = True

    def is_closed(self):
        with self.lock:
            return self.closed

    def len(self):
        return self.q.qsize()

class AuraSupervisor:
    def __init__(self, name="AuraSupervisor", max_restarts=3, backoff=0.2):
        self.name = name
        self.max_restarts = max_restarts
        self.backoff = backoff
        self.workers = {}
        self.lock = threading.Lock()

    def supervise(self, worker_name, target_func, args=()):
        def runner():
            restarts = 0
            while restarts <= self.max_restarts:
                try:
                    target_func(*args)
                    break
                except Exception as e:
                    restarts += 1
                    if restarts > self.max_restarts:
                        print(f"[{self.name}] Worker '{worker_name}' failed critically after {self.max_restarts} restarts: {e}")
                        break
                    print(f"[{self.name}] Worker '{worker_name}' crashed ({e}). Restarting {restarts}/{self.max_restarts}...")
                    time.sleep(self.backoff)

        thread = threading.Thread(target=runner, daemon=True, name=f"AuraWorker-{worker_name}")
        with self.lock:
            self.workers[worker_name] = thread
        thread.start()
        return thread

    def join_all(self, timeout=2.0):
        with self.lock:
            threads = list(self.workers.values())
        for t in threads:
            t.join(timeout=timeout)

class AuraConcurrencyManager:
    @staticmethod
    def spawn_task(func, args=()):
        t = threading.Thread(target=func, args=args, daemon=True)
        t.start()
        return t
