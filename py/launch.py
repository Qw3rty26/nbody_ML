import argparse
from multiprocessing import Pool
from simulation_batch import run
import logging
from logger_settings import configure_logging
import time

def run_wrapper(args):
    return run(*args)

def main():

    parser = argparse.ArgumentParser(
        description="Generate Plummer clusters"
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


    args = parser.parse_args()

    configure_logging(args.verbose, args.debug)

    logger = logging.getLogger(__name__)

    simulation_args = [
        (
            simulation_id,
            args.stars,
            args.integrator,
            args.dt,
            args.output
        )
        for simulation_id in range(args.simulations)
    ]

    logger.info(f"------------------------------------------")
    logger.info(f"         STARTING BATCH EXECUTION         ")
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
        for completed, _ in enumerate(pool.imap_unordered(run_wrapper, simulation_args), 1):
            logger.info(f"\033[32mProgress: {completed}/{args.simulations} Simulations completed\033[0m")
    computing_time = time.perf_counter() - computing_time
    logger.info(f"------------------------------------------")
    logger.info(f"         BATCH EXECUTION COMPLETED        ")
    logger.info(f"")
    logger.info(f"  EXECUTION TIME: {computing_time:.3f} seconds")
    logger.info(f"")
    logger.info(f"------------------------------------------")


if __name__ == "__main__":
    main()
