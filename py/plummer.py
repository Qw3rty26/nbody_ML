import numpy as np
import scipy.optimize as so

GRAVITATIONAL_CONSTANT = 1
CLUSTER_MASS = 1

class Plummer:

   def __init__(self, plummer_radius = 0, number_of_stars = 0):
      self.plummer_radius = plummer_radius
      self.number_of_stars = number_of_stars

   def _density_rho(self, radius_from_center):

      #              3 * M * a^2
      # rho = ----------------------------
      #        4 * pi * (a^2 + r^2)^(5/2)

      numerator = 3 * CLUSTER_MASS * (self.plummer_radius ** 2)

      denominator = 4 * np.pi * ( (self.plummer_radius ** 2 + radius_from_center**2) ** (5 / 2))

      rho = numerator / denominator
      return rho

   def _potential_phi(self, radius_from_center):

      #             G * M
      # phi = -----------------
      #        sqrt(a^2 + r^2)

      numerator = GRAVITATIONAL_CONSTANT * CLUSTER_MASS

      denominator = np.sqrt(self.plummer_radius**2 + radius_from_center**2)

      phi = - numerator / denominator
      return phi

   def _enclosed_mass(self, radius_from_center):

      #              M * r^3
      # mass = ------------------
      #         (a^2 + r^2)^(3/2)

      numerator = CLUSTER_MASS * radius_from_center**3

      denominator = (self.plummer_radius**2 + radius_from_center**2) ** (3 / 2)

      mass = numerator / denominator
      return mass

   def _sample_radius(self):
      # given u, solve:
      # M(r) - u = 0
      # for r

      mass_fraction_u = np.random.rand()

      def equation(radius):
         return self._enclosed_mass(radius) - mass_fraction_u

      radius_guess = self.plummer_radius # good starting guess

      sampled_radius = so.fsolve(equation, radius_guess)[0]

      return sampled_radius

   def _random_versor(self):
      versor = np.random.normal(size = 3) # generate a random point in 3D space
      norm = np.linalg.norm(versor) # normalise the versor so that its length is 1
      if norm == 0:
         return versor
      else:
         return versor / norm

   def _sample_velocity(self, radius_from_center):
      return np.zeros(3)

   def generate_plummer_cluster(self):
      positions = []
      velocities = []

      for i in range(self.number_of_stars):

         radius = self._sample_radius()
         versor = self._random_versor()
         xyz = radius * versor
         positions.append(xyz)

         v = self._sample_velocity(radius)
         velocities.append(v)

      return np.array(positions), np.array(velocities)
