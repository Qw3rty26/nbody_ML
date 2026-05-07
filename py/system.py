import entity
import threading
import time

class System:
    def __init__(self):
        #self.space =
        self.entity = []
        self.paused = True

    def startLoop(self, handler):  # physicsLoop is in a thread and runs constantly
        self.sse_handler = handler
        if hasattr(self, "thread") and self.thread.is_alive():
            return  # return because thread is already running
        self.thread = threading.Thread(target=self.physicsLoop)
        self.thread.daemon = True
        self.thread.start()

    def physicsLoop(self):
        while True:
            if not self.paused:
                #run physics engine
                try:
                    print("tick")
                    self.sse_handler.wfile.write(b"data: tick\n\n")
                    self.sse_handler.wfile.flush()
                except (BrokenPipeError, ConnectionResetError, OSError):
                    print("SSE client disconnected")
                    self.sse_handler = None
                    self.paused = True
                    break
            time.sleep(1)

    def start(self):
	    self.paused = False

    def pause(self):
	    print("fired a pause")
	    self.paused = True

    def clear(self):
        self.entity.clear()

    def update(self, timestep=0): # updates entities based on the timestep given
        if timestep <= 0:
            return
        for e in self.entity:
            e.update(timestep)

    def render(self): # returns a JSON object containing an array of entities' data
        return {
            "entities": [e.render() for e in self.entity]
        }

    def addEntity(self, x=0, y=0, xVel=0, yVel=0, mass=0): # adds a new entity
        newEntity = entity.Entity(x, y, xVel, yVel, mass)
        self.entity.append(newEntity)

    def removeEntity(self, entity):
        if entity in self.entity:
            self.entity.remove(entity)
