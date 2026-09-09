import argparse
import logging
import time
import json
import os
from multiprocessing import Pool

from simulation_batch import run_cluster_generation as run_gen
from simulation_batch import run_galaxy_tidal_stripping as run_gts
from logger_settings import configure_logging


def run_gen_wrapper(args):
    return run_gen(*args)


def run_gts_wrapper(args):
    return run_gts(*args)


def load_configuration_JSON(file_path):
    with open(file_path, "r") as file:
        return json.load(file)


def _generate_clusters(logger, configuration, simulation_args):
    simulation = configuration["Simulation"]
    cluster = configuration["Cluster Generation"]
    output = configuration["Output"]

    logger.info("------------------------------------------")
    logger.info("           GENERATING CLUSTERS")
    logger.info("")
    logger.info(f"  NO. SIMULATIONS: {len(simulation_args)}")
    logger.info(f"  STARS: {cluster['stars']}")
    logger.info(f"  STARTING TIME: {cluster['starting_time']}")
    logger.info(f"  DT: {simulation['dt']}")
    logger.info(f"  G: {simulation['G']}")
    logger.info(f"  SOFTENING: {simulation['softening']}")
    logger.info(f"  TIME WARP: {simulation['time_warp']}")
    logger.info(f"  INTEGRATOR: {simulation['integrator']}")
    logger.info(f"  OUTPUT: {output['cluster_json']}/")
    logger.info("")
    logger.info("------------------------------------------")

    computing_time = time.perf_counter()

    with Pool() as pool:
        for completed, _ in enumerate(
            pool.imap_unordered(run_gen_wrapper, simulation_args),
            1
        ):
            logger.info(
                f"\033[32mProgress: "
                f"{completed}/{len(simulation_args)} "
                f"Clusters generated.\033[0m"
            )

    computing_time = time.perf_counter() - computing_time

    logger.info("------------------------------------------")
    logger.info("        CLUSTER GENERATION COMPLETED")
    logger.info("")
    logger.info(f"  EXECUTION TIME: {computing_time:.3f} seconds")
    logger.info("")
    logger.info("------------------------------------------")


def _simulate_gts(logger, configuration, simulation_args):
    simulation = configuration["Simulation"]
    gts = configuration["Galactic Tidal Stripping"]
    output = configuration["Output"]

    logger.info("------------------------------------------")
    logger.info("            EVOLVING GALAXY")
    logger.info("")
    logger.info(f"  NO. SIMULATIONS: {len(simulation_args)}")
    logger.info(f"  INTEGRATOR: {simulation['integrator']}")
    logger.info(f"  DT: {simulation['dt']}")
    logger.info(f"  GALAXY MASS: {gts['galaxy_mass']}")
    logger.info(f"  GALAXY RADIUS: {gts['galaxy_radius']}")
    logger.info(f"  NUMBER OF ORBITS: {gts['number_of_orbits']}")
    logger.info(f"  OUTPUT: {output['gts_xyzv']}/")
    logger.info("")
    logger.info("------------------------------------------")

    computing_time = time.perf_counter()

    with Pool() as pool:
        for completed, _ in enumerate(
            pool.imap_unordered(run_gts_wrapper, simulation_args),
            1
        ):
            logger.info(
                f"\033[32mProgress: "
                f"{completed}/{len(simulation_args)} "
                f"Simulations completed.\033[0m"
            )

    computing_time = time.perf_counter() - computing_time

    logger.info("------------------------------------------")
    logger.info("         GALAXY EVOLUTION COMPLETED")
    logger.info("")
    logger.info(f"  EXECUTION TIME: {computing_time:.3f} seconds")
    logger.info("")
    logger.info("------------------------------------------")


def main():

    parser = argparse.ArgumentParser(
        description="Generate Plummer clusters and simulate galactic tidal strippings"
    )

    parser.add_argument(
        "--config",
        type=str,
        default="../configuration.json",
        help="path to configuration file"
    )

    parser.add_argument(
        "--verbose",
        action="store_true",
        help="enable verbose output"
    )

    parser.add_argument(
        "--debug",
        action="store_true",
        help="enable debug output"
    )

    args = parser.parse_args()

    configuration = load_configuration_JSON(args.config)

    configure_logging(args.verbose, args.debug)

    logger = logging.getLogger(__name__)

    simulation = configuration["Simulation"]
    cluster = configuration["Cluster Generation"]
    gts = configuration["Galactic Tidal Stripping"]
    experiment = configuration["Experiment"]
    output = configuration["Output"]

    os.makedirs(output["cluster_json"], exist_ok=True)
    os.makedirs(output["cluster_xyzv"], exist_ok=True)
    os.makedirs(output["gts_xyzv"], exist_ok=True)
    os.makedirs(output["results"], exist_ok=True)

    if experiment["parameter"] == "cluster_radius":
        simulation_args = []

        cluster_id = 0

        for cluster_radius in experiment["values"]:
            for _ in range(experiment["simulations_per_value"]):
                simulation_args.append(
                    (
                        cluster_id,
                        cluster_radius,
                        cluster["stars"],
                        cluster["starting_time"],
                        simulation["dt"],
                        simulation["G"],
                        simulation["softening"],
                        simulation["time_warp"],
                        simulation["integrator"],
                        output["cluster_json"],
                    )
                )

                cluster_id += 1
    else:
        raise ValueError(
            f"Unsupported experiment parameter: {experiment['parameter']}"
        )

    answer = input("\n\nGenerate new clusters? [Y/N]")

    if answer.lower() == "y":
        _generate_clusters(
            logger,
            configuration,
            simulation_args
        )

    cluster_files = [
        os.path.join(output["cluster_json"], file)
        for file in os.listdir(output["cluster_json"])
        if file.endswith(".json")
    ]

    gts_args = [
        (
            cluster_file,
            gts["galaxy_mass"],
            gts["galaxy_radius"],
            gts["number_of_orbits"],
            output["gts_xyzv"],
        )
        for cluster_file in cluster_files
    ]

    answer = input("\n\nSimulate clusters in the galaxy? [Y/N]")

    if answer.lower() == "y":
        _simulate_gts(
            logger,
            configuration,
            gts_args
        )


if __name__ == "__main__":
    main()
