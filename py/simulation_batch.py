from simulation import Simulation
from plummer import Plummer
import numpy as np
import json

# MAGIC NUMBERS
NUMBER_OF_STARS = 10
RADIUS = 3
STAR_MASS = 1.0 / NUMBER_OF_STARS
END_TIME = 10 * RADIUS ** (3 / 2) / np.sqrt(NUMBER_OF_STARS)


def create_simulation():
   plummer = Plummer(RADIUS, NUMBER_OF_STARS)
   sim = Simulation()

   positions, velocities = plummer.generate_plummer_cluster()

   for x, v in zip(positions, velocities):
      sim.add_entity(
         x[0], x[1], x[2],
         v[0], v[1], v[2],
         STAR_MASS
      )

   sim.cluster_diagnostics.set_initial_total_energy()

   return sim

def evolve_cluster(sim):
   next_cleanup = 1.0

   while sim.simulation.t < END_TIME:
      sim.update()

      if sim.simulation.t >= next_cleanup:
         sim.clean_cluster()
         next_cleanup += 1.0


def save_cluster(sim):
   #sim.save_to_file("prova.bin")
   snapshot = sim.get_snapshot()

   with open("prova.txt", "w") as file:
      json.dump(snapshot, file, indent=4)

def run():

   sim = create_simulation()

   evolve_cluster(sim)

   save_cluster(sim)


if __name__ == "__main__":
    run()
