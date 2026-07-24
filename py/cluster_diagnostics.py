import numpy as np

class ClusterDiagnostics:

    def __init__(self, simulation):
        if simulation is None:
           raise ValueError("object simulation is None")

        self.simulation = simulation
        self.initial_total_energy = None

    def get_center_of_mass(self):
       return self.simulation.com()

    def set_initial_total_energy(self):
       self.initial_total_energy = self.simulation.energy()

    def get_initial_total_energy(self):
       return self.initial_total_energy

    def get_total_energy_relative_error(self):
       if self.initial_total_energy is None:
          raise ValueError("initial total energy cannot be None")

       current_total_energy = self.simulation.energy()

       #                      |E(t) - E_0|
       # relative_error(t) = --------------
       #                         |E_0|

       numerator = abs(current_total_energy - self.initial_total_energy)

       denominator = abs(self.initial_total_energy)

       total_energy_relative_error = numerator / denominator

       return total_energy_relative_error

    def get_half_mass_radius(self):

       com = self.get_center_of_mass()

       distances = []

       for p in self.simulation.particles:
          dx = p.x - com.x
          dy = p.y - com.y
          dz = p.z - com.z

          r = np.sqrt(dx*dx + dy*dy + dz*dz)

          distances.append(r)

       distances.sort()
       half_index = len(distances) // 2

       return distances[half_index]


    def get_snapshot(self):
       com = self.get_center_of_mass()
       snapshot = { # returns a JSON object containing an array of cluster diagnostic data
          "initial_energy": self.get_initial_total_energy(),
          "error_energy": self.get_total_energy_relative_error(),
          "half_mass_radius": self.get_half_mass_radius(),
          "center_of_mass": {
             "x": com.x,
             "y": com.y,
             "z": com.z
          }
       }
       return snapshot

