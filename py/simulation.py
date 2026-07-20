import time
import json
import rebound
import numpy as np

class Simulation:

    def __init__(self):
        self.simulation = rebound.Simulation()
        self.simulation.integrator = "whfast"
        self.simulation.G = 1.0
        self.simulation.t = 0
        self.time_warp = 100
        self.simulation.dt = 1e-4
        self.simulation.softening = 0.01

    def update(self):
       if len(self.simulation.particles) < 1:
          return

       for _ in range(self.time_warp):
          self.simulation.integrate(self.simulation.t + self.simulation.dt)

    def get_snapshot(self):
       #com, half_mass_radius = [0,0,0], 10
       #com, half_mass_radius = self.get_half_mass_radius()
       snapshot = { # returns a JSON object containing an array of entities' data
          #"half_mass_radius": half_mass_radius,
          #"center_of_mass": com,
          "time": self.simulation.t,
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

    def add_entity(self, xPos=0, yPos=0, zPos=0, xVel=0, yVel=0, zVel=0, mass=0):
        self.simulation.add(
           m = mass,
           x = xPos,
           y = yPos,
           z = zPos,
           vx = xVel,
           vy = yVel,
           vz = zVel
        )

    def remove_entity(self, id):
       self.simulation.remove(id)
