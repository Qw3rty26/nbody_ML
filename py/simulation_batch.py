from simulation import Simulation
from plummer import Plummer
import numpy as np
import json
import os

# MAGIC NUMBERS
RADIUS = 5

def create_simulation(simulation_id, number_of_stars):
   np.random.seed(simulation_id)
   STAR_MASS = 1.0 / number_of_stars

   plummer = Plummer(RADIUS, number_of_stars)
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

def evolve_cluster(sim, end_time):
   next_cleanup = 1.0

   while sim.simulation.t < end_time:
      sim.update()

      if sim.simulation.t >= next_cleanup:
         sim.clean_cluster()
         next_cleanup += 1.0


def save_cluster(sim, simulation_id, output_path):
   os.makedirs(output_path, exist_ok=True)

   #sim.save_to_file(f"{output_path}/cluster_{simulation_id}.bin")
   snapshot = sim.get_snapshot()

   with open(f"{output_path}/cluster_{simulation_id}.txt", "w") as file:
      json.dump(snapshot, file, indent=4)

def run(simulation_id = 0, number_of_stars = 1, output_path = "default"):
   sim = create_simulation(simulation_id, number_of_stars)

   END_TIME = 10 * RADIUS ** (3 / 2) / np.sqrt(number_of_stars)

   evolve_cluster(sim, END_TIME)

   save_cluster(sim, simulation_id, output_path)

