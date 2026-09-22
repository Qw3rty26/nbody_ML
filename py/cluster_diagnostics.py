import numpy as np
import logging

logger = logging.getLogger(__name__)

GRAVITATIONAL_CONSTANT = 1

class ClusterDiagnostics:

    def __init__(self, simulation):

        if simulation is None:
           raise ValueError("object simulation is None")

        self.simulation = simulation
        self.rebound_simulation = simulation.simulation
        self.initial_total_energy = None
        self.initial_angular_momentum = None
        self.orbital_angle = self.get_cluster_orbital_angle()
        self.total_rotation = 0
        self.orbits = 0

    def get_center_of_mass(self):
       return self.rebound_simulation.com()

    def get_cluster_orbits(self):
        return self.orbits

    def get_cluster_orbital_angle(self):
        center_of_mass = self.get_center_of_mass()

        numerator = 180 * np.arctan2(center_of_mass.y, center_of_mass.x)

        denominator = np.pi

        orbital_angle = numerator / denominator

        return orbital_angle

    def update_orbital_angle(self):

        # assuming center of galaxy is at (0, 0, 0)
        new_angle = self.get_cluster_orbital_angle()

        center_of_mass = self.get_center_of_mass()

        radius = np.sqrt(
            center_of_mass.x**2 +
            center_of_mass.y**2 +
            center_of_mass.z**2
        )

        rotation = new_angle - self.orbital_angle

        if rotation < -180:
            rotation += 360
        elif rotation > 180:
            rotation -= 360

        self.total_rotation += abs(rotation)

        if abs(self.total_rotation) >= 360:
            self.orbits += 1

            if self.total_rotation >= 360:
                self.total_rotation -= 360
            else:
                self.total_rotation += 360

        self.orbital_angle = new_angle

    def get_galactic_potential_energy(self):

        #                     G * M_gal * m_i
        # U_gal = - sum_i ( --------------------- )
        #                     sqrt(a^2 + r_i^2)

        if self.simulation.galactic_potential is None:
            return 0.0

        total_potential_energy = 0.0

        for entity in self.rebound_simulation.particles:

            radius_i_squared = (
                entity.x**2 +
                entity.y**2 +
                entity.z**2
            )

            numerator = GRAVITATIONAL_CONSTANT * self.simulation.galactic_potential.get_galaxy_mass() * entity.m

            denominator = np.sqrt( self.simulation.galactic_potential.get_galaxy_radius()**2 + radius_i_squared )

            total_potential_energy += numerator / denominator

        total_potential_energy *= -1

        return total_potential_energy


    def get_total_energy(self):

        #
        # E = K + U_cluster + U_gal
        #

        total_energy = self.rebound_simulation.energy()

        total_energy += self.get_galactic_potential_energy()

        return total_energy

    def set_initial_total_energy(self):
       self.initial_total_energy = self.get_total_energy()

    def get_initial_total_energy(self):
       return self.initial_total_energy

    def get_total_energy_relative_error(self):

        #                                   |E(t) - E_0|
        # total_energy_relative_error(t) = --------------
        #                                      |E_0|

        if self.initial_total_energy is None:
            raise ValueError("Initial total energy cannot be None")

        if self.initial_total_energy == 0:
            logger.warning("Initial total energy is 0")
            return 0.0

        current_total_energy = self.get_total_energy()

        numerator = abs(current_total_energy - self.initial_total_energy)

        denominator = abs(self.initial_total_energy)

        total_energy_relative_error = numerator / denominator

        return total_energy_relative_error

    def get_total_energy_relative_error_percentage(self):
        total_energy_relative_error_percentage = self.get_total_energy_relative_error() * 100
        return total_energy_relative_error_percentage

    def get_total_angular_momentum(self):

        # L_internal = sum((r_i - r_COM) x m_i * (v_i - v_COM))

        center_of_mass = self.rebound_simulation.com()

        total_angular_momentum = np.zeros(3)

        for entity in self.rebound_simulation.particles:

            position = np.array([
                entity.x - center_of_mass.x,
                entity.y - center_of_mass.y,
                entity.z - center_of_mass.z
            ])

            velocity = np.array([
                entity.vx - center_of_mass.vx,
                entity.vy - center_of_mass.vy,
                entity.vz - center_of_mass.vz
            ])

            total_angular_momentum += entity.m * np.cross(position, velocity)

        return total_angular_momentum

    def set_initial_angular_momentum(self):
       self.initial_angular_momentum = self.get_total_angular_momentum()

    def get_initial_angular_momentum(self):
       return self.initial_angular_momentum

    def get_total_angular_momentum_error(self):

        #                                             |L(t) - L_0|
        # total_angular_momentum_relative_error(t) = --------------
        #                                                 |L_0|

        current_total_angular_momentum = self.get_total_angular_momentum()

        numerator = np.linalg.norm(
            current_total_angular_momentum - self.initial_angular_momentum
        )

        denominator = np.linalg.norm(self.initial_angular_momentum)


        total_angular_momentum_error = numerator / denominator

        return total_angular_momentum_error

    def get_total_angular_momentum_error_percentage(self):
        total_angular_momentum_error_percentage = self.get_total_angular_momentum_error() * 100
        return total_angular_momentum_error_percentage

    def get_half_mass_radius(self):

       com = self.get_center_of_mass()

       distances = []

       for p in self.rebound_simulation.particles:
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
       # potential_energy_i = - G * sum_j!=i( ------------- )
       #                                       distance_ij

       entity_potential_energy = 0.0

       for entity_j in self.rebound_simulation.particles:
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

       entity_potential_energy = - GRAVITATIONAL_CONSTANT * entity_potential_energy

       return entity_potential_energy

    def get_entity_total_energy(self, entity):

       #
       # total_energy_i = kinetic_energy_i + potential_energy_i
       #

       entity_kinetic_energy = self.get_entity_kinetic_energy(entity)
       entity_potential_energy = self.get_entity_potential_energy(entity)
       if self.simulation.galactic_potential is not None:
           radius = np.sqrt(
               entity.x**2 +
               entity.y**2 +
               entity.z**2
           )

           entity_potential_energy += (
               entity.m * self.simulation.galactic_potential._potential_phi(radius)
           )

       entity_total_energy = entity_kinetic_energy + entity_potential_energy

       return entity_total_energy

    def get_escaped_entity_ids(self):

       escaped_entity_ids = []

       for entity in self.rebound_simulation.particles:
          entity_total_energy = self.get_entity_total_energy(entity)

          if entity_total_energy > 0:
             escaped_entity_ids.append(entity.name)

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

