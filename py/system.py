from sse import SSE
from simulation import Simulation
import threading
import time

class System:
    def __init__(self):
        self.tick = 0
        self.sse = None
        self.simulation = Simulation()
        #threading
        self.running = False
        self.paused = True
        self.thread = None
        #threading

    # PHYSICS LOOP
    def createPhysicsLoop(self):
       if self.running:
          return False

       self.thread = threading.Thread(target = self.physicsLoop, daemon = True)
       self.running = True
       self.thread.start()
       return True

    def destroyPhysicsLoop(self):
       self.running = False

       if self.thread:
          self.thread.join(timeout=1)

       self.thread = None
       self.paused = True
       return True

    def physicsLoop(self):
       while self.running:
          if not self.paused:
             self.simulation.update()
             self.tick += 1
             if self.tick % 60 == 0:
                self.tick = 0
                self.sse.write(self.simulation.getSnapshot())
          time.sleep(0.016)

    def startPhysicsLoop(self):
       self.paused = False

    def pausePhysicsLoop(self):
       self.paused = True
    # PHYSICS LOOP

    # SSE
    def connectSSE(self, handler):
       self.sse = SSE(handler);

    def disconnectSSE(self):
       self.sse = None;
    # SSE
