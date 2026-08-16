import rebound

from cluster_diagnostics import ClusterDiagnostics


class Simulation:

    def __init__(
        self,
        dt=1e-3,
        t=0,
        G=1.0,
        softening=0,
        time_warp=1,
        integrator="whfast"
    ):
        self.simulation = rebound.Simulation()
        self.cluster_diagnostics = ClusterDiagnostics(self.simulation)
        self.galactic_potential = None

        self.simulation.dt = dt
        self.simulation.t = t
        self.simulation.G = G
        self.simulation.softening = softening
        self.simulation.integrator = integrator

        self.time_warp = time_warp

    def update(self):
        for _ in range(self.time_warp):
            self.simulation.integrate(
                self.simulation.t + self.simulation.dt
            )

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

    def add_galaxy_forces_wrapper(self, _):
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
                x=entity["x"],
                y=entity["y"],
                z=entity["z"],
                vx=entity["vx"],
                vy=entity["vy"],
                vz=entity["vz"],
                mass=entity["mass"]
            )

        if self.galactic_potential is not None:
            self.move_cluster(
                4 * self.galactic_potential.get_galaxy_radius(),
                0,
                0
            )

    def get_JSON_snapshot(self):
        snapshot = {
            "time": self.simulation.t,
            "dt": self.simulation.dt,
            "G": self.simulation.G,
            "softening": self.simulation.softening,
            "time_warp": self.time_warp,
            "integrator": str(self.simulation.integrator),
            "entities": [{
                "id": i,
                "x": p.x,
                "y": p.y,
                "z": p.z,
                "vx": p.vx,
                "vy": p.vy,
                "vz": p.vz,
                "mass": p.m
            } for i, p in enumerate(self.simulation.particles)]
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
                f"t={self.simulation.t} "
                f"dt={self.simulation.dt} "
                f"M={self.galactic_potential.get_galaxy_mass()} "
                f"a={self.galactic_potential.get_galaxy_radius()}"
            )
            snapshot.append(
                "O 0 0 0 "
                "0 0 0"
            )
        else:
            snapshot.append(
                f"Plummer star cluster "
                f"t={self.simulation.t} "
                f"dt={self.simulation.dt}"
            )

        for particle in self.simulation.particles:
            snapshot.append(
                f"H {particle.x} {particle.y} {particle.z} "
                f"{particle.vx} {particle.vy} {particle.vz}"
            )

        return snapshot

    def save_to_file(self, file_name):
        if file_name is None:
            raise ValueError("file name cannot be None")

        self.simulation.save_to_file(file_name)

    def clear(self):
        self.__init__()

    def add_entity(
        self,
        x=0,
        y=0,
        z=0,
        vx=0,
        vy=0,
        vz=0,
        mass=0.1
    ):
        self.simulation.add(
            m=mass,
            x=x,
            y=y,
            z=z,
            vx=vx,
            vy=vy,
            vz=vz
        )

    def remove_entity(self, entity_id):
        self.simulation.remove(entity_id)

    def clean_cluster(self):
        number_of_escaped_entities = 0
        escaped_entity_ids = (
            self.cluster_diagnostics.get_escaped_entity_ids()
        )

        for entity_id in reversed(escaped_entity_ids):
            self.simulation.remove(entity_id)
            number_of_escaped_entities += 1

        return number_of_escaped_entities

    def move_to_center_of_mass(self):
        self.simulation.move_to_com()
