import rebound

from cluster_diagnostics import ClusterDiagnostics


class Simulation:

    def __init__(self, dt, G, softening, time_warp, integrator):

        self.simulation = rebound.Simulation()
        self.galactic_potential = None
        self.cluster_diagnostics = ClusterDiagnostics(self)

        self.simulation.dt = dt
        self.simulation.t = 0
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

    def _apply_galactic_forces(self, _):

        self.galactic_potential.add_galaxy_forces(
            self.simulation.particles
        )

    def add_galactic_potential(self, galactic_potential):

        self.galactic_potential = galactic_potential
        self.simulation.additional_forces = self._apply_galactic_forces

    def load_JSON_snapshot(self, snapshot):

        self.simulation.t = snapshot["time"]
        self.simulation.dt = snapshot["dt"]
        self.simulation.G = snapshot["G"]
        self.simulation.softening = snapshot["softening"]
        self.time_warp = snapshot["time_warp"]
        self.simulation.integrator = snapshot["integrator"]

        for entity in snapshot["entities"]:
            self.add_entity(
                x=entity["x"],
                y=entity["y"],
                z=entity["z"],
                vx=entity["vx"],
                vy=entity["vy"],
                vz=entity["vz"],
                mass=entity["mass"],
                id = entity["id"]
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
                "mass": p.m,
                "id": p.name
            } for i, p in enumerate(self.simulation.particles)]
        }

        return snapshot

    def get_XYZV_snapshot(self):

        snapshot = []

        if self.galactic_potential is not None:
            snapshot.append(len(self.simulation.particles) + 2)
        else:
            snapshot.append(len(self.simulation.particles) + 1)

        if self.galactic_potential is not None:
            snapshot.append(
                f"Galactic Tidal Stripped Cluster "
                f"Properties=species:S:1:id:I:1:pos:R:3:vel:R:3 "
                f"t={self.simulation.t} "
                f"dt={self.simulation.dt} "
                f"M={self.galactic_potential.get_galaxy_mass()} "
                f"a={self.galactic_potential.get_galaxy_radius()} "
            )
            snapshot.append(
                "O 10000 0 0 0 "
                "0 0 0"
            )
        else:
            snapshot.append(
                f"Plummer Star Cluster "
                f"Properties=species:S:1:id:I:1:pos:R:3:vel:R:3 "
                f"t={self.simulation.t} "
                f"dt={self.simulation.dt}"
            )
        com = self.cluster_diagnostics.get_center_of_mass()

        snapshot.append(
            f"C 9999 {com.x} {com.y} {com.z} "
            f"{com.vx} {com.vy} {com.vz} "
        )

        for particle in self.simulation.particles:
            snapshot.append(
                f"H {particle.name} {particle.x} {particle.y} {particle.z} "
                f"{particle.vx} {particle.vy} {particle.vz}"
            )

        return snapshot

    def add_entity(self, x=0, y=0, z=0, vx=0, vy=0, vz=0, mass=0.1, id=0):

        self.simulation.add(x=x, y=y, z=z, vx=vx, vy=vy, vz=vz, m=mass, name=str(id))


    def remove_entity(self, entity_id):

        self.simulation.remove(entity_id)

    def clean_escaped_stars(self, escaped_entity_ids):

        for entity_id in escaped_entity_ids:
            self.simulation.remove(entity_id)

        return len(escaped_entity_ids)
