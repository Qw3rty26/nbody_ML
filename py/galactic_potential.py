import numpy as np

GRAVITATIONAL_CONSTANT = 1


class GalacticPotential:

    def __init__(self, plummer_radius = 1, plummer_mass = 1):
        if plummer_radius <= 0:
            raise ValueError("plummer_radius must be greater than 0")

        if plummer_mass <= 0:
            raise ValueError("plummer_mass must be greater than 0")

        self.plummer_radius = plummer_radius   # a
        self.plummer_mass = plummer_mass # M

    def get_galaxy_radius(self):
        return self.plummer_radius

    def get_galaxy_mass(self):
        return self.plummer_mass

    def _potential_phi(self, radius_from_center):

        #               - G * M
        # phi(r) = -----------------
        #           sqrt(a^2 + r^2)

        numerator = -1 * GRAVITATIONAL_CONSTANT * self.plummer_mass

        denominator = np.sqrt(self.plummer_radius**2 + radius_from_center**2)

        phi = numerator / denominator
        return phi

    def _acceleration(self, x, y, z):

        #                   - G * M
        # a_x = ------------------------------- * x
        #        (a^2 + x^2 + y^2 + z^2)^(3/2)
        #
        #                   - G * M
        # a_y = ------------------------------- * y
        #        (a^2 + x^2 + y^2 + z^2)^(3/2)
        #
        #                   - G * M
        # a_z = ------------------------------- * z
        #        (a^2 + x^2 + y^2 + z^2)^(3/2)

        numerator = -GRAVITATIONAL_CONSTANT * self.plummer_mass

        radius_squared = x**2 + y**2 + z**2
        denominator = ( self.plummer_radius**2 + radius_squared )**(1.5)

        acceleration_factor = numerator / denominator

        acceleration_x = acceleration_factor * x
        acceleration_y = acceleration_factor * y
        acceleration_z = acceleration_factor * z

        return acceleration_x, acceleration_y, acceleration_z

    def get_cluster_initial_velocity(self, radius):

        #               G * M * r^2
        # v = sqrt( ------------------- )
        #            (a^2 + r^2)^(3/2)

        numerator = ( GRAVITATIONAL_CONSTANT * self.plummer_mass * radius**2 )

        denominator = ( self.plummer_radius**2 + radius**2 )**(1.5)

        velocity = np.sqrt( numerator / denominator )
        return velocity


    def add_galaxy_forces(self, particles):

        size = len(particles)
        x = np.empty(size)
        y = np.empty(size)
        z = np.empty(size)

        for i, p in enumerate(particles):
            x[i], y[i], z[i] = p.x, p.y, p.z

        ax, ay, az = self._acceleration(x, y, z)

        for i, particle in enumerate(particles):

            particle.ax += ax[i]
            particle.ay += ay[i]
            particle.az += az[i]
