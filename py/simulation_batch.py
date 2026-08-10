from simulation import Simulation
from plummer import Plummer
from galactic_potential import GalacticPotential
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

    sim.move_to_center_of_mass()
    sim.cluster_diagnostics.set_initial_total_energy()

    return sim

def save_cluster_with_snapshots(sim, file):
    snapshot = sim.get_XYZV_snapshot()
    for line in snapshot:
        file.write(f"{line}\n")

def clean_cluster_with_snapshots(sim, end_time, file):
    next_cleanup = 1.0
    next_snapshot = 0.01
    escaped_entities = 0

    while sim.simulation.t < end_time:
        sim.update()

        if sim.simulation.t >= next_snapshot:
            save_cluster_with_snapshots(sim, file)
            next_snapshot += 0.01

        if sim.simulation.t >= next_cleanup:
            escaped_entities += sim.clean_cluster()
            next_cleanup += 1.0

    return escaped_entities

def evolve_cluster(sim, end_time, file):

    while sim.simulation.t < end_time:
        sim.update()
    save_cluster_with_snapshots(sim, file)

def clean_cluster(sim, end_time):
    next_cleanup = 1.0
    escaped_entities = 0

    while sim.simulation.t < end_time:
       sim.update()

       if sim.simulation.t >= next_cleanup:
          escaped_entities += sim.clean_cluster()
          next_cleanup += 1.0

    return escaped_entities


def save_cluster(sim, simulation_id, output_path):
    os.makedirs(output_path+"/JSON", exist_ok=True)

    #sim.save_to_file(f"{output_path}/cluster_{simulation_id}.bin")
    snapshot = sim.get_JSON_snapshot()
    with open(f"{output_path}/JSON/cluster_{simulation_id}.json", "w") as file:
       json.dump(snapshot, file, indent=4)

    #snapshot = sim.get_XYZV_snapshot()
    #with open(f"{output_path}/cluster_{simulation_id}.xyzv", "w") as file:
    #    for line in snapshot:
    #        file.write(f"{line}\n")

def run_gen(simulation_id = 0, number_of_stars = 1, integrator = "whfast", dt = 1e-3, output_path = "default"):
    logger.debug(f"Simulation {simulation_id}: Started!")
    sim = create_simulation(simulation_id, number_of_stars, integrator, dt)

    END_TIME = 10 * RADIUS ** (3 / 2) / np.sqrt(number_of_stars)
    os.makedirs(output_path, exist_ok=True)
    logger.debug(f"Simulation {simulation_id}: Evolving cluster...")
    with open(f"{output_path}/cluster_{simulation_id}.xyzv", "w") as file:
        escaped_entities = clean_cluster_with_snapshots(sim, END_TIME, file)
    save_cluster(sim, simulation_id, output_path)
    logger.info(f"Simulation {simulation_id}: {escaped_entities} Stars removed.")


def run_gts(cluster_file, galaxy_mass=10, galaxy_radius=1, integrator="whfast", dt=1e-3, output_path="default" ):
    logger.debug(f"Simulation {cluster_file}: Started!")

    with open(cluster_file, "r") as file:
        snapshot = json.load(file)

    sim = Simulation(
        dt=snapshot["dt"],
        integrator=snapshot["integrator"]
    )

    galactic_potential = GalacticPotential(
        galaxy_radius,
        galaxy_mass
    )

    sim.add_galactic_potential(galactic_potential)

    sim.load_JSON_snapshot(snapshot)

    logger.debug(f"Simulation {cluster_file}: Cluster loaded.")

    END_TIME = 100
    os.makedirs(output_path, exist_ok=True)

    cluster_name = os.path.splitext(
         os.path.basename(cluster_file)
     )[0]

    output_file = os.path.join(
        output_path,
        f"{cluster_name}.xyzv"
    )

    with open(output_file, "w") as file:
        evolve_cluster(sim, END_TIME, file)
