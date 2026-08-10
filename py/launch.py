import argparse
from multiprocessing import Pool
from simulation_batch import run_gen
from simulation_batch import run_gts
import logging
from logger_settings import configure_logging
import time
import os

def run_gen_wrapper(args):
    return run_gen(*args)

def run_gts_wrapper(args):
    return run_gts(*args)

def get_cluster_files(input_path):
    return sorted(
        path for path in os.listdir(input_path)
        if path.endswith(".json")
    )

def _generate_clusters(logger, args, simulation_args):
    logger.info(f"------------------------------------------")
    logger.info(f"       STARTING CLUSTER GENERATION        ")
    logger.info(f"")
    logger.info(f"  NO. SIMULATIONS: {args.simulations}")
    logger.info(f"  STARS: {args.stars}")
    logger.info(f"  INTEGRATOR: {args.integrator}")
    logger.info(f"  DT: {args.dt}")
    logger.info(f"  OUTPUT: {args.output}/")
    logger.info(f"")
    logger.info(f"------------------------------------------")

    computing_time = time.perf_counter()
    with Pool() as pool:
        for completed, _ in enumerate(pool.imap_unordered(run_gen_wrapper, simulation_args), 1):
            logger.info(f"\033[32mProgress: {completed}/{args.simulations} Simulations completed\033[0m")
    computing_time = time.perf_counter() - computing_time
    logger.info(f"------------------------------------------")
    logger.info(f"        CLUSTER GENERATION COMPLETED      ")
    logger.info(f"")
    logger.info(f"  EXECUTION TIME: {computing_time:.3f} seconds")
    logger.info(f"")
    logger.info(f"------------------------------------------")


def _simulate_gts(logger, args, simulation_args):
    logger.info(f"------------------------------------------")
    logger.info(f"       STARTING GALACTIC SIMULATIONS        ")
    logger.info(f"")
    logger.info(f"  NO. SIMULATIONS: {args.simulations}")
    logger.info(f"  INTEGRATOR: {args.integrator}")
    logger.info(f"  DT: {args.dt}")
    logger.info(f"  OUTPUT: {args.output}/gts/")
    logger.info(f"  GALAXY MASS: {args.galaxy_mass}")
    logger.info(f"  GALAXY RADIUS: {args.galaxy_radius}")
    logger.info(f"")
    logger.info(f"------------------------------------------")

    computing_time = time.perf_counter()
    with Pool() as pool:
        for completed, _ in enumerate(pool.imap_unordered(run_gts_wrapper, simulation_args), 1):
            logger.info(f"\033[32mProgress: {completed}/{len(simulation_args)} Simulations completed\033[0m")
    computing_time = time.perf_counter() - computing_time
    logger.info(f"------------------------------------------")
    logger.info(f"        CLUSTER GENERATION COMPLETED      ")
    logger.info(f"")
    logger.info(f"  EXECUTION TIME: {computing_time:.3f} seconds")
    logger.info(f"")
    logger.info(f"------------------------------------------")
def main():

    parser = argparse.ArgumentParser(
        description="Generate Plummer clusters and simulate galactic tidal strippings"
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

    parser.add_argument(
        "--stars",
        type=int,
        default=256,
        help="number of stars"
    )

    parser.add_argument(
        "--galaxy_mass",
        type=int,
        default=10,
        help="mass of the galaxy"
    )

    parser.add_argument(
        "--galaxy_radius",
        type=int,
        default=2,
        help="radius of the galaxy"
    )

    parser.add_argument(
        "--simulations",
        type=int,
        default=1,
        help="number of simulations"
    )

    parser.add_argument(
        "--integrator",
        choices=["leapfrog", "whfast", "ias15"],
        default="whfast",
        help="select integrator"
    )

    parser.add_argument(
        "--dt",
        type=float,
        default=1e-3,
        help="select timestep integration"
    )

    parser.add_argument(
        "--output",
        type=str,
        default="clusters",
        help="output directory"
    )

    parser.add_argument(
        "--input",
        type=str,
        default="clusters",
        help="input directory"
    )

    args = parser.parse_args()

    configure_logging(args.verbose, args.debug)

    logger = logging.getLogger(__name__)

    simulation_args = [
        (
            simulation_id,
            args.stars,
            args.integrator,
            args.dt,
            args.output,
        )
        for simulation_id in range(args.simulations)
    ]

    answer = input("\n\nGenerate new clusters? [Y/N]")
    if answer.lower() == "y":
        _generate_clusters(logger, args, simulation_args)

    cluster_files = [
        os.path.join(args.output, "JSON", file)
        for file in os.listdir(os.path.join(args.output, "JSON"))
            if file.endswith(".json")
    ]

    gts_output_path = os.path.join(args.output, "gts")

    gts_args = [
        (
            cluster_file,
            args.galaxy_mass,
            args.galaxy_radius,
            args.integrator,
            args.dt,
            gts_output_path,
        )
        for cluster_file in cluster_files
    ]

    answer = input("\n\nSimulate clusters in the galaxy? [Y/N]")
    if answer.lower() == "y":
        _simulate_gts(logger, args, gts_args)


if __name__ == "__main__":
    main()

