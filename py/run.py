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

def create_run_directory(output_path, create_clst, create_gts):

    run_id = 1

    while os.path.exists(os.path.join(output_path, f"run_{run_id:03d}")):
        run_id += 1

    if create_clst.lower() == "y"  or create_gts.lower() == "y":
        run_path = os.path.join(output_path, f"run_{run_id:03d}")

    if create_clst.lower() == "y":
        os.makedirs(os.path.join(run_path, "GEN", "JSON"))
        os.makedirs(os.path.join(run_path, "GEN", "XYZV"))

    if create_gts.lower() == "y":
        os.makedirs(os.path.join(run_path, "GTS", "JSON"))
        os.makedirs(os.path.join(run_path, "GTS", "XYZV"))

    return run_path


def _generate_clusters(logger, configuration, simulation_args):

    simulation = configuration["simulation"]
    cluster = configuration["cluster generation"]
    output = configuration["output directory"]

    logger.info("------------------------------------------")
    logger.info("           GENERATING CLUSTERS")
    logger.info("")
    logger.info(f"  NO. SIMULATIONS: {len(simulation_args)}")
    logger.info(f"  STARS: {cluster['number_of_stars']}")
    logger.info(f"  DT: {simulation['dt']}")
    logger.info(f"  G: {simulation['G']}")
    logger.info(f"  SOFTENING: {simulation['softening']}")
    logger.info(f"  TIME WARP: {simulation['time_warp']}")
    logger.info(f"  INTEGRATOR: {simulation['integrator']}")
    logger.info(f"  OUTPUT: {output}/")
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

    simulation = configuration["simulation"]
    gts = configuration["galactic tidal stripping"]
    output = configuration["output directory"]

    logger.info("------------------------------------------")
    logger.info("            EVOLVING GALAXY")
    logger.info("")
    logger.info(f"  NO. SIMULATIONS: {len(simulation_args)}")
    logger.info(f"  INTEGRATOR: {simulation['integrator']}")
    logger.info(f"  DT: {simulation['dt']}")
    logger.info(f"  GALAXY MASS: {gts['galaxy_mass']}")
    logger.info(f"  GALAXY RADIUS: {gts['galaxy_radius']}")
    logger.info(f"  NUMBER OF ORBITS: {gts['number_of_orbits']}")
    logger.info(f"  OUTPUT: {output}/")
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

    simulation = configuration["simulation"]
    cluster = configuration["cluster generation"]
    gts = configuration["galactic tidal stripping"]

    simulation_args = []
    run_path = None
    cluster_files = None
    cluster_json = None
    cluster_xyzv = None
    gts_json = None
    gts_xyzv = None

    cluster_answer = input("\n\nGenerate new clusters? [Y/N]")
    gts_answer = input("\n\nSimulate clusters in the galaxy? [Y/N]")

    if cluster_answer.lower() == "y":
        run_path = create_run_directory(configuration["output directory"], cluster_answer, gts_answer)

        cluster_json = os.path.join(run_path, "GEN", "JSON")
        cluster_xyzv = os.path.join(run_path, "GEN", "XYZV")

        for cluster_id in range(cluster["number_of_clusters"]):
            simulation_args.append(
                (
                    cluster_id,
                    cluster["cluster_radius"],
                    cluster["number_of_stars"],
                    simulation["dt"],
                    simulation["G"],
                    simulation["softening"],
                    simulation["time_warp"],
                    simulation["integrator"],
                    cluster_json,
                    cluster_xyzv
                )
            )

        _generate_clusters(logger, configuration, simulation_args)
    else:
        print("can't simulate GTS without generating the cluster first. exiting...")
        exit()

    cluster_files = [
        os.path.join(cluster_json, file)
        for file in os.listdir(cluster_json)
        if file.endswith(".json")
    ]

    if gts_answer.lower() == "y":
        if run_path is None:
            run_path = create_run_directory(configuration["output directory"], cluster_answer, gts_answer)
        gts_json = os.path.join(run_path, "GTS", "JSON")
        gts_xyzv = os.path.join(run_path, "GTS", "XYZV")

        gts_args = [
            (
                cluster_file,
                gts["galaxy_mass"],
                gts["galaxy_radius"],
                gts["number_of_orbits"],
                gts_json,
                gts_xyzv
            )
            for cluster_file in cluster_files
        ]

        _simulate_gts(logger, configuration, gts_args)


if __name__ == "__main__":
    main()
