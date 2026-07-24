import time
import json
import rebound
import numpy as np

class Simulation:

    def __init__(self):
        self.simulation = rebound.Simulation()
        self.initial_energy = None
        self.energy_error = 0
        self.simulation.integrator = "whfast"
        self.simulation.G = 1.0
        self.simulation.t = 0
        self.time_warp = 1
        self.simulation.dt = 1e-1
        self.simulation.softening = 0

    def update(self):
       if len(self.simulation.particles) < 1:
          return

       for _ in range(self.time_warp):
          self.simulation.integrate(self.simulation.t + self.simulation.dt)

       self.check_energy_conservation()


    def get_snapshot(self):
       #com, half_mass_radius = [0,0,0], 10
       #com, half_mass_radius = self.get_half_mass_radius()
       snapshot = { # returns a JSON object containing an array of entities' data
          #"half_mass_radius": half_mass_radius,
          #"center_of_mass": com,
          "time": self.simulation.t,
          "dt": self.simulation.dt,
          "initial_energy": self.initial_energy,
          "error_energy": self.energy_error,
          "half_mass_radius": self.get_half_mass_radius(),
          "center_of_mass": {
             "x": self.com[0],
             "y": self.com[1],
             "z": self.com[2]
          },
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

    def set_initial_energy(self):
       self.initial_energy = self.simulation.energy()

    def check_energy_conservation(self):
       if self.initial_energy is None:
          return None

       current_energy = self.simulation.energy()

       self.energy_error = abs(
          (current_energy - self.initial_energy)
          #/ self.initial_energy
       )

    def get_half_mass_radius(self):

       particles = self.simulation.particles

       if len(particles) == 0:
           return 0

       com_x = 0
       com_y = 0
       com_z = 0
       total_mass = 0

       for p in particles:
          com_x += p.m * p.x
          com_y += p.m * p.y
          com_z += p.m * p.z
          total_mass += p.m

       com_x /= total_mass
       com_y /= total_mass
       com_z /= total_mass

       self.com = [com_x, com_y, com_z]

       distances = []

       for p in particles:
          dx = p.x - com_x
          dy = p.y - com_y
          dz = p.z - com_z

          r = np.sqrt(dx*dx + dy*dy + dz*dz)

          distances.append(r)

       distances.sort()
       half_index = len(distances) // 2

       return distances[half_index]
