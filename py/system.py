import entity
import threading
import time
import json

class System:
    def __init__(self):
        #self.space =
        self.dt = 0.016
        self.entity = []
        self.paused = True

    def _update(self):
        for e in self.entity:
            e.update(self.dt)

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
                try:
                    payload = { # returns a JSON object containing an array of entities' data
                        "entities": [e.getJSON() for e in self.entity]
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
        self.entity.clear()

    def addEntity(self, x=0, y=0, xVel=0, yVel=0, mass=0): # adds a new entity
        newEntity = entity.Entity(x, y, xVel, yVel, mass)
        self.entity.append(newEntity)

    def removeEntity(self, entity):
        if entity in self.entity:
            self.entity.remove(entity)
