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

    def get_particle_kinetic_energy(self, particle):

       #                     1
       # kinetic_energy_i = --- m_i v_i^2
       #                     2

       particle_kinetic_energy = 0.5 * particle.m * (
          particle.vx**2 +
          particle.vy**2 +
          particle.vz**2
       )

       return particle_kinetic_energy

    def get_particle_potential_energy(self, particle_i):

       #                                        m_i * m_j
       # potential_energy_i = - G * sum_j!=i( -------------)
       #                                       distance_ij

       particle_potential_energy = 0.0

       for particle_j in self.simulation.particles:
          if particle_j is particle_i: # j != i
             continue

          distance_x = particle_i.x - particle_j.x
          distance_y = particle_i.y - particle_j.y
          distance_z = particle_i.z - particle_j.z

          distance = np.sqrt(
             distance_x**2 +
             distance_y**2 +
             distance_z**2
          )

          if distance == 0:
             continue

          particle_potential_energy += (
             particle_i.m *
             particle_j.m /
             distance
          )

       particle_potential_energy = - self.simulation.G * particle_potential_energy

       return particle_potential_energy

    def get_particle_total_energy(self, particle):

       #
       # total_energy_i = kinetic_energy_i + potential_energy_i
       #

       particle_total_energy = self.get_particle_kinetic_energy(particle) + self.get_particle_potential_energy(particle)

       return particle_total_energy

    def get_escaped_particles_ids(self):
       escaped_particles_ids = []

       for id, particle in enumerate(self.simulation.particles):
          particle_total_energy = self.get_particle_total_energy(particle)

          if particle_total_energy > 0:
             escaped_particles_ids.append(id)

       return escaped_particles_ids

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

