from sse import SSE
from threading import Thread
from multiprocessing import Process, Queue
import time
from simulation_runner import run
from queue import Empty

class System:
    def __init__(self):
       self.sse = None
       self.process = None
       self.commands_queue = Queue()
       self.snapshot_queue = Queue()

    def create_physics_loop(self):
       self.process = Process(target = run, args = (self.commands_queue, self.snapshot_queue,))
       if not self.process: return False
       self.process.start()

    def destroy_physics_loop(self):
       if self.process is None:
          raise RuntimeError("Physics process not created")
       self.commands_queue.put("exit")
       self.process.join(timeout=2)
       if self.process.is_alive():
          self.process.terminate()
          self.process.join()


    def start_physics_loop(self):
       self.commands_queue.put("start")

    def pause_physics_loop(self):
       self.commands_queue.put("pause")

    def connect_sse(self, handler):
       print("called connect SSE")
       self.sse = SSE(handler)
       self.sse.write({"status": "connected"})

       if hasattr(self, "listener_thread"):
          return

       self.listener_thread = Thread(
          target=self.snapshot_listener,
          daemon=True
       )
       self.listener_thread.start()

    def snapshot_listener(self):
       while True:
          try:
             data = self.snapshot_queue.get()
             self.sse.write(data)

          except Exception:
             break

    def disconnect_sse(self):
       print(f"called disconnect SSE")
       self.sse.close()
