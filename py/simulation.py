from cluster_diagnostics import ClusterDiagnostics
import rebound


class Simulation:

    def initialize_simulation(self, dt = 1e-3, integrator = "whfast"):
        self.simulation.t = 0
        self.simulation.G = 1.0
        self.simulation.dt = dt
        self.simulation.softening = 0
        self.simulation.integrator = integrator
        self.time_warp = 10

    def __init__(self, dt = 1e-3, integrator = "whfast"):
        self.simulation = rebound.Simulation()
        self.cluster_diagnostics = ClusterDiagnostics(self.simulation)
        self.galactic_potential = None
        self.initialize_simulation(dt, integrator)

    def update(self):
        for _ in range(self.time_warp):
            self.simulation.integrate(self.simulation.t + self.simulation.dt)

    def move_cluster(self, moved_x, moved_y, moved_z):
        for particle in self.simulation.particles:
            particle.x += moved_x
            particle.y += moved_y
            particle.z += moved_z

    def speed_cluster(self, speed_x, speed_y, speed_z):
        for particle in self.simulation.particles:
            particle.vx += speed_x
            particle.vy += speed_y
            particle.vz += speed_z

    def add_galaxy_forces_wrapper(self, reb_sim):
        self.galactic_potential.add_galaxy_forces(
            self.simulation.particles
        )

    def add_galactic_potential(self, galactic_potential):
        self.galactic_potential = galactic_potential
        self.simulation.additional_forces = self.add_galaxy_forces_wrapper

    def load_JSON_snapshot(self, snapshot):
        self.simulation.t = snapshot["time"]

        for entity in snapshot["entities"]:
            self.add_entity(
                xPos=entity["xPos"],
                yPos=entity["yPos"],
                zPos=entity["zPos"],
                xVel=entity["xVel"],
                yVel=entity["yVel"],
                zVel=entity["zVel"],
                mass=entity["mass"]
            )
            self.move_cluster(
                4 * self.galactic_potential.get_galaxy_radius(),
                0,
                0
            )
            self.add_entity(
                xPos=entity["xPos"],
                yPos=entity["yPos"],
                zPos=entity["zPos"],
                xVel=entity["xVel"],
                yVel=entity["yVel"],
                zVel=entity["zVel"],
                mass=entity["mass"]
            )
            self.move_cluster(
                0,
                4 * self.galactic_potential.get_galaxy_radius(),
                0
            )
            self.add_entity(
                xPos=entity["xPos"],
                yPos=entity["yPos"],
                zPos=entity["zPos"],
                xVel=entity["xVel"],
                yVel=entity["yVel"],
                zVel=entity["zVel"],
                mass=entity["mass"]
            )
            self.move_cluster(
                -4 * self.galactic_potential.get_galaxy_radius(),
                0,
                0
            )
            self.add_entity(
                xPos=entity["xPos"],
                yPos=entity["yPos"],
                zPos=entity["zPos"],
                xVel=entity["xVel"],
                yVel=entity["yVel"],
                zVel=entity["zVel"],
                mass=entity["mass"]
            )
            self.move_cluster(
                0,
                -4 * self.galactic_potential.get_galaxy_radius(),
                0
            )

    def get_JSON_snapshot(self):
        #diagnostics = self.cluster_diagnostics.get_snapshot()
        snapshot = { # returns a JSON object containing an array of entities' data
            #**diagnostics,
            "time": self.simulation.t,
            "dt": self.simulation.dt,
            "integrator": str(self.simulation.integrator),
            "entities": [{
                "id": i,
                "xPos": p.x,
                "yPos": p.y,
                "zPos": p.z,
                "xVel": p.vx,
                "yVel": p.vy,
                "zVel": p.vz,
                "mass": p.m
                #"totalenergy": self.cluster_diagnostics.get_entity_total_energy(p)
            }for i, p in enumerate(self.simulation.particles)]
        }
        return snapshot

    def get_XYZV_snapshot(self):
        snapshot = []

        if self.galactic_potential is not None:
            snapshot.append(len(self.simulation.particles) + 1)
        else:
            snapshot.append(len(self.simulation.particles))

        if self.galactic_potential is not None:
            snapshot.append(
                f"t={self.simulation.t} dt={self.simulation.dt} M={self.galactic_potential.get_galaxy_mass()} a={self.galactic_potential.get_galaxy_radius()}"
            )
        else:
            snapshot.append(
                f"Plummer star cluster t={self.simulation.t} dt={self.simulation.dt}"
            )

        if self.galactic_potential is not None:
            snapshot.append(
                f"O 0 0 0 "
                f"0 0 0"
        )
        for i, p in enumerate(self.simulation.particles):
            snapshot.append(
                f"H {p.x} {p.y} {p.z} "
                f"{p.vx} {p.vy} {p.vz}"
            )

        return snapshot

    def save_to_file(self, file_name):
       if file_name is None:
           raise ValueError("file name cannot be None")
       self.simulation.save_to_file(file_name)

    def clear(self):
        self.simulation = rebound.Simulation()
        self.cluster_diagnostics = ClusterDiagnostics(self.simulation)
        self.initialize_simulation()

    def add_entity(self, xPos=0, yPos=0, zPos=0, xVel=0, yVel=0, zVel=0, mass=0.1):
        self.simulation.add(
            m = mass,
            x = xPos,
            y = yPos,
            z = zPos,
            vx = xVel,
            vy = yVel,
            vz = zVel
        )

    def remove_entity(self, entity_id):
       self.simulation.remove(entity_id)

    def clean_cluster(self):
        number_of_escaped_entities = 0
        escaped_entity_ids = self.cluster_diagnostics.get_escaped_entity_ids()

        for entity_id in reversed(escaped_entity_ids):
            self.simulation.remove(entity_id)
            number_of_escaped_entities += 1

        return number_of_escaped_entities


    def move_to_center_of_mass(self):
        self.simulation.move_to_com()
