import time
from queue import Empty

from simulation import Simulation
from plummer import Plummer


def handle_command(command, state):
   if command == "start":
      state["is_paused"] = False

   elif command == "pause":
      state["is_paused"] = True

   elif command == "exit":
      state["is_running"] = False

   elif command == "reset":
      ...

def run(command_queue, snapshot_queue):
   #print(f"child process is running", flush=True)
   NUMBER_OF_STARS = 512
   RADIUS = 4
   STAR_MASS = 1.0 / NUMBER_OF_STARS

   plummer = Plummer(RADIUS, NUMBER_OF_STARS)

   END_TIME = 10 * plummer.plummer_radius ** (3 / 2)
   SLEEP_TIME = 0.016

   sim = Simulation()

   positions, velocities = plummer.generate_plummer_cluster()

   for x, v in zip(positions, velocities):
      sim.add_entity(
         x[0], x[1], x[2],
         v[0], v[1], v[2],
         STAR_MASS
      )

   state = {
      "is_running": True,
      "is_paused": True
   }

   sim.set_initial_energy()
   snapshot_queue.put(sim.get_snapshot())

   while state["is_running"]:

      try:
         cmd = command_queue.get_nowait()
         handle_command(cmd, state)
      except Empty:
         pass

      if sim.simulation.t > END_TIME:
         break

      if not state["is_paused"]:
         sim.update()
         snapshot_queue.put(sim.get_snapshot())

      time.sleep(SLEEP_TIME)
