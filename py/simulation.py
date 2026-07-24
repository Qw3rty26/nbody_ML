from cluster_diagnostics import ClusterDiagnostics
import json
import rebound


class Simulation:

    def __init__(self):
        self.simulation = rebound.Simulation()
        self.cluster_diagnostics = ClusterDiagnostics(self.simulation)


        # MAGIC NUMBERS
        self.simulation.integrator = "whfast"
        self.simulation.G = 1.0
        self.simulation.t = 0
        self.time_warp = 1
        self.simulation.dt = 1e-1
        self.simulation.softening = 0

    def update(self):
       for _ in range(self.time_warp):
          self.simulation.integrate(self.simulation.t + self.simulation.dt)

    def get_snapshot(self):
       diagnostics = self.cluster_diagnostics.get_snapshot()
       snapshot = { # returns a JSON object containing an array of entities' data
          **diagnostics,
          "time": self.simulation.t,
          "dt": self.simulation.dt,
          "entities": [{
             "id": i,
             "xPos": p.x,
             "yPos": p.y,
             "zPos": p.z,
             "xVel": p.vx,
             "yVel": p.vy,
             "zVel": p.vz,
             "mass": p.m,
             "totalenergy": self.cluster_diagnostics.get_particle_total_energy(p)
          }for i, p in enumerate(self.simulation.particles)]
       }
       return snapshot

    def save_to_file(self, file_name):
       if file_name is None:
          raise ValueError("file name cannot be None")
       self.simulation.save_to_file(file_name)

    def clear(self):
        self.simulation = rebound.Simulation()
        self.cluster_diagnostics = ClusterDiagnostics(self.simulation)

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

    def clean_cluster(self):
       escaped_stars_ids = self.cluster_diagnostics.get_escaped_particles_ids()

       for particle_id in reversed(escaped_stars_ids):
          self.simulation.remove(particle_id)
