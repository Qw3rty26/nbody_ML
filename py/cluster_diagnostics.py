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

    def get_entity_kinetic_energy(self, entity):

       #                     1
       # kinetic_energy_i = --- m_i v_i^2
       #                     2

       entity_kinetic_energy = 0.5 * entity.m * (
          entity.vx**2 +
          entity.vy**2 +
          entity.vz**2
       )

       return entity_kinetic_energy

    def get_entity_potential_energy(self, entity_i):

       #                                        m_i * m_j
       # potential_energy_i = - G * sum_j!=i( -------------)
       #                                       distance_ij

       entity_potential_energy = 0.0

       for entity_j in self.simulation.particles:
          if entity_j is entity_i: # j != i
             continue

          distance_x = entity_i.x - entity_j.x
          distance_y = entity_i.y - entity_j.y
          distance_z = entity_i.z - entity_j.z

          distance = np.sqrt(
             distance_x**2 +
             distance_y**2 +
             distance_z**2
          )

          if distance == 0:
             continue

          entity_potential_energy += (
             entity_i.m *
             entity_j.m /
             distance
          )

       entity_potential_energy = - self.simulation.G * entity_potential_energy

       return entity_potential_energy

    def get_entity_total_energy(self, entity):

       #
       # total_energy_i = kinetic_energy_i + potential_energy_i
       #

       entity_kinetic_energy = self.get_entity_kinetic_energy(entity)
       entity_potential_energy = self.get_entity_potential_energy(entity)

       entity_total_energy = entity_kinetic_energy + entity_potential_energy

       return entity_total_energy

    def get_escaped_entity_ids(self):
       escaped_entity_ids = []

       for entity_id, entity in enumerate(self.simulation.particles):
          entity_total_energy = self.get_entity_total_energy(entity)

          if entity_total_energy > 0:
             escaped_entity_ids.append(entity_id)

       return escaped_entity_ids

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

