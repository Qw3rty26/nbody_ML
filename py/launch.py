import argparse
from multiprocessing import Pool
from simulation_batch import run


def main():

    parser = argparse.ArgumentParser(
        description="Generate Plummer clusters"
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
        "--workers",
        type=int,
        default=None,
        help="number of parallel workers"
    )

    parser.add_argument(
        "--output",
        type=str,
        default="clusters",
        help="output directory"
    )


    args = parser.parse_args()


    simulation_args = [
        (
            simulation_id,
            args.stars,
            args.output
        )
        for simulation_id in range(args.simulations)
    ]


    with Pool(args.workers) as pool:
        pool.starmap(run, simulation_args)



if __name__ == "__main__":
    main()
