import time
import json
import rebound

class Simulation:
    def __init__(self):
        self.simulation = rebound.Simulation()
        self.simulation.integrator = "leapfrog"
        self.simulation.G = 1.0
        self.simulation.t = 0
        self.timeWarp = 6
        self.simulation.dt = 1e-4
        self.simulation.softening = 0.01

    def update(self):
       if len(self.simulation.particles) < 1:
          return

       for _ in range(self.timeWarp):
          self.simulation.integrate(self.simulation.t + self.simulation.dt)

    def getSnapshot(self):
       snapshot = { # returns a JSON object containing an array of entities' data
          "entities": [{
             "id": i,
             "xPos": p.x,
             "yPos": p.y,
             "zPos": p.z,
             "xVel": p.vx,
             "yVel": p.vy,
             "zVel": p.vz,
             "mass": p.m
          }for i, p in enumerate(self.simulation.particles)]
       }
       return snapshot

    def clear(self):
        self.simulation = rebound.Simulation()

    def addEntity(self, xPos=0, yPos=0, zPos=0, xVel=0, yVel=0, zVel=0, mass=0):
        self.simulation.add(
           m = mass,
           x = xPos,
           y = yPos,
           z = zPos,
           vx = xVel,
           vy = yVel,
           vz = zVel
        )

    def removeEntity(self, id):
       self.simulation.remove(id)
