from multiprocessing import Pool as pool

from simulation_batch import run

NUMBER_OF_SIMULATIONS = 100


if __name__ == "__main__":
   pool.map(run, range(NUMBER_OF_SIMULATIONS))
