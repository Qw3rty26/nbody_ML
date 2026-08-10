from simulation import Simulation
from plummer import Plummer
from galactic_potential import GalacticPotential
import logging
import numpy as np
import json
import os

logger = logging.getLogger(__name__)

def generate_cluster(cluster_id, cluster_radius, number_of_stars, integrator, dt):
    np.random.seed(cluster_id)
    STAR_MASS = 1.0 / number_of_stars

    logger.debug(f"Cluster no. {cluster_id}: Generating Plummer Cluster...")
    plummer = Plummer(cluster_radius, number_of_stars)
    positions, velocities = plummer.generate_plummer_cluster()

    simulation = Simulation(dt, integrator)

    for pos, vel in zip(positions, velocities):
       simulation.add_entity(
          pos[0], pos[1], pos[2],
          vel[0], vel[1], vel[2],
          STAR_MASS
       )

    simulation.move_to_center_of_mass()
    simulation.cluster_diagnostics.set_initial_total_energy()

    return simulation

def save_snapshot_XYZV(simulation, file):
    snapshot = simulation.get_XYZV_snapshot()
    for line in snapshot:
        file.write(f"{line}\n")

def save_snapshot_JSON(simulation, file):
    snapshot = simulation.get_JSON_snapshot()
    json.dump(snapshot, file, indent=4)

def clean_cluster(simulation, end_time, xyzv_path):
    next_cleanup = 1.0
    next_snapshot = 0.01
    escaped_entities = 0

    with open(xyzv_path, "w") as xyzv_file:
        while simulation.simulation.t < end_time:
            simulation.update()

            if simulation.simulation.t >= next_snapshot:
                save_snapshot_XYZV(simulation, xyzv_file)
                next_snapshot += 0.01

            if simulation.simulation.t >= next_cleanup:
                escaped_entities += simulation.clean_cluster()
                next_cleanup += 1.0

    if escaped_entities != 0:
        logger.debug(f"Cleaned {escaped_entities} stars.")

def evolve_cluster(simulation, end_time):
    while simulation.simulation.t < end_time:
        simulation.update()

def run_cluster_generation(
    cluster_id = 0,
    cluster_radius = 1,
    number_of_stars = 0,
    integrator = "whfast",
    dt = 1e-3,
    output_path = "./clusters"
):
        logger.info(f"Cluster no. {cluster_id}: Generating...")
        simulation = generate_cluster(
            cluster_id,
            cluster_radius,
            number_of_stars,
            integrator,
            dt
        )

        END_TIME = 10 * cluster_radius ** (3 / 2) / np.sqrt(number_of_stars)

        os.makedirs(output_path, exist_ok=True)
        xyzv_path = os.path.join(
            output_path,
            f"cluster_{cluster_id}.xyzv"
        )

        json_path = os.path.join(
            output_path,
            f"cluster_{cluster_id}.json"
        )
        logger.debug(f"Cluster no. {cluster_id}: Cleaning...")
        clean_cluster(simulation, END_TIME, xyzv_path)
        with open(json_path, "w") as json_file:
            save_snapshot_JSON(simulation, json_file)
        logger.debug(f"Cluster no. {cluster_id}: Done.")


def run_galaxy_tidal_stripping(
    cluster_file,
    galaxy_mass=10,
    galaxy_radius=1,
    integrator="whfast",
    dt=1e-3,
    output_path="./clusters/gts"
):
        logger.info(f"Simulation {cluster_file}: Running...")

        with open(cluster_file, "r") as json_file:
            snapshot = json.load(json_file)

        simulation = Simulation(
            dt=snapshot["dt"],
            integrator=snapshot["integrator"]
        )

        galactic_potential = GalacticPotential(galaxy_radius, galaxy_mass)
        simulation.add_galactic_potential(galactic_potential)


        logger.debug(f"Simulation {cluster_file}: Loading...")
        simulation.load_JSON_snapshot(snapshot)

        END_TIME = 100

        logger.debug(f"Simulation {cluster_file}: Evolving...")
        evolve_cluster(simulation, END_TIME)

        cluster_name = os.path.splitext(
            os.path.basename(cluster_file)
        )[0]

        os.makedirs(output_path, exist_ok=True)
        output_file = os.path.join(
            output_path,
            f"{cluster_name}.xyzv"
        )

        with open(output_file, "w") as xyzv_file:
            save_snapshot_XYZV(simulation, xyzv_file)

        logger.debug(f"Simulation {cluster_file}: Done.")
