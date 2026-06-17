import threading
import time
import json
import rebound

class System:
    def __init__(self):
        self.simulation = rebound.Simulation()
        self.simulation.G = 1.0;
        self.dt = 0.016
        self.simulation.dt = self.dt;
        self.tick = 0
        self.paused = True

    def _update(self):
       if self.paused:
          return

       if len(self.simulation.particles) < 1:
          return
       self.tick += 1
       self.simulation.integrate(self.simulation.t + self.dt)

    def startSSE(self, handler):  # SSELoop is in a thread and runs constantly
        self.paused = False
        self.sse_handler = handler
        if hasattr(self, "thread") and self.thread.is_alive():
            return  # return because thread is already running
        self.thread = threading.Thread(target=self.SSELoop)
        self.thread.daemon = True
        self.thread.start()

    def SSELoop(self):
        while True: # loop indefinitely
            if not self.paused:
                self._update()
                if self.tick % 60 == 0:
                    self.tick = 0
                    try:
                        payload = { # returns a JSON object containing an array of entities' data
                           "entities": [
                              {
                                 "id": i,
                                 "xPos": p.x,
                                 "yPos": p.y,
                                 "zPos": p.z,
                                 "xVel": p.vx,
                                 "yVel": p.vy,
                                 "zVel": p.vz,
                                 "mass": p.m
                              }
                           for i, p in enumerate(self.simulation.particles)
                           ]
                        }

                        self.sse_handler.wfile.write( # write into the stream
                            f"data: {json.dumps(payload)}\n\n".encode()
                        )
                        self.sse_handler.wfile.flush()

                    except (BrokenPipeError, ConnectionResetError, OSError): # if SSE connection is closed, reloaded or an error occurs
                        print("SSE client disconnected")
                        self.clearSystem()
                        self.sse_handler = None
                        self.paused = True
                        break

            time.sleep(self.dt)

    def pauseSSE(self):
	    self.paused = True

    def unpauseSSE(self):
            self.paused = False

    def clearSystem(self):
        self.simulation = rebound.Simulation()

    def addEntity(self, xPos=0, yPos=0, zPos=0, xVel=0, yVel=0, zVel=0, mass=0): # adds a new entity
        self.simulation.add(
           m = mass,
           x = xPos,
           y = yPos,
           z = zPos,
           vx = xVel,
           vy = yVel,
           vz = zVel
        )

    def removeEntity(self, id):  # removes an entity
       self.simulation.remove(id)

    def setTimestep(self, timestep):
        if timestep > 0:
            self.dt = timestep
