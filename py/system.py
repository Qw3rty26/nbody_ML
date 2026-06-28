from sse import SSE
from multiprocessing import Process, Queue
from simulation import physics_loop
import time

class System:
    def __init__(self):
       self.sse = None
       self.process = None
       self.queue = Queue()

    def create_physics_loop(self):
       self.process = Process(target = physics_loop, args = (self.queue,))

    def destroy_physics_loop(self):
       if self.process is None:
          raise RuntimeError("Physics process not created")

       self.process.terminate()
       self.process.join()

    def start_physics_loop(self):
       if not self.process: return False
       self.process.start()
       while True:
          if self.sse and not self.queue.empty():
             data = self.queue.get()
             try:
                self.sse.write(data)
             except Exception as e:
                self.destroyPhysicsLoop()
                break;

       #send add through a pipe

    def pause_physics_loop(self):
       pass
       #send pause through a pipe

    def connect_sse(self, handler):
       self.sse = SSE(handler)
       self.sse.write({"type": "connected"})

    def disconnect_sse(self):
       print(f"called disconnect SSE")
       self.sse.close()
