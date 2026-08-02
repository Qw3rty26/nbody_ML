from simulation import Simulation
from plummer import Plummer
import logging
import numpy as np
import json
import os

logger = logging.getLogger(__name__)

# MAGIC NUMBERS
RADIUS = 5

def create_simulation(simulation_id, number_of_stars, integrator, dt):
    np.random.seed(simulation_id)
    STAR_MASS = 1.0 / number_of_stars

    logger.debug(f"Simulation {simulation_id}: Generating Plummer cluster...")
    plummer = Plummer(RADIUS, number_of_stars)
    logger.debug(f"Simulation {simulation_id}: Plummer cluster generated.")
    sim = Simulation(dt, integrator)

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
    escaped_entities = 0

    while sim.simulation.t < end_time:
       sim.update()

       if sim.simulation.t >= next_cleanup:
          escaped_entities += sim.clean_cluster()
          next_cleanup += 1.0

    return escaped_entities


def save_cluster(sim, simulation_id, output_path):
    os.makedirs(output_path, exist_ok=True)

    #sim.save_to_file(f"{output_path}/cluster_{simulation_id}.bin")
    snapshot = sim.get_snapshot()

    with open(f"{output_path}/cluster_{simulation_id}.txt", "w") as file:
       json.dump(snapshot, file, indent=4)

def run(simulation_id = 0, number_of_stars = 1, integrator = "leapfrog", dt = 1e-3, output_path = "default"):
    logger.debug(f"Simulation {simulation_id}: Started!")
    sim = create_simulation(simulation_id, number_of_stars, integrator, dt)

    END_TIME = 10 * RADIUS ** (3 / 2) / np.sqrt(number_of_stars)


    logger.debug(f"Simulation {simulation_id}: Evolving cluster...")
    escaped_entities = evolve_cluster(sim, END_TIME)
    logger.info(f"Simulation {simulation_id}: {escaped_entities} Stars removed.")

    logger.debug(f"Simulation {simulation_id}: Saving output in {output_path}/cluster_{simulation_id}.txt")
    save_cluster(sim, simulation_id, output_path)
    logger.debug(f"Simulation {simulation_id}: Done!")
