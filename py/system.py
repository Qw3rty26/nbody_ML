from sse import SSE
from multiprocessing import Process, Queue
from simulation import physicsLoop
import time

class System:
    def __init__(self):
       self.sse = None
       self.process = None
       self.queue = Queue()

    def createPhysicsLoop(self):
       self.process = Process(target = physicsLoop, args = (self.queue,))

    def destroyPhysicsLoop(self):
       if self.process is None:
          raise RuntimeError("Physics process not created")

       self.process.terminate()
       self.process.join()

    def startPhysicsLoop(self):
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

    def pausePhysicsLoop(self):
       pass
       #send pause through a pipe

    def connectSSE(self, handler):
       self.sse = SSE(handler)
       self.sse.write({"type": "connected"})

    def disconnectSSE(self):
       print(f"called disconnect SSE")
       self.sse.close()
