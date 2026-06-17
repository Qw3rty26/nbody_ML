class System{
	constructor(maxX=0, maxY=0){
		this.space = new space(0, 0, maxX, maxY, 100);
		this.properties = new properties();
		this.gravity = new gravity();
		this.newEntities = [];
                this.oldEntities = [];
		this.lastSnapshotTime = performance.now();
	}

	pauseSSE(){
		fetch("http://127.0.0.1:8000/simulation/pauseSSE", {
                        method: "GET",
                        headers: { "Content-Type": "application/json" },
                })
	}

	unpauseSSE(){
                fetch("http://127.0.0.1:8000/simulation/unpauseSSE", {
                        method: "GET",
                        headers: { "Content-Type": "application/json" },
                })
        }

	clearSystem(){
		fetch("http://127.0.0.1:8000/simulation/clearSystem", {
                        method: "GET",
                        headers: { "Content-Type": "application/json" },
                })
	}

	addEntity(xPos=0, yPos=0, zPos=0, xVel=0, yVel=0, zVel=0, mass=0){
		fetch("http://127.0.0.1:8000/simulation/add_entity", {
                        method: "POST",
                        headers: { "Content-Type": "application/json" },
                        body: JSON.stringify({xPos, yPos, zPos, xVel, yVel, zVel, mass})
                })
        }

	removeEntity(index){
		//POST fetch
	}

	setTimestep(timestep = 0.016){
                fetch("http://127.0.0.1:8000/simulation/set_timestep", {
                        method: "POST",
                        headers: { "Content-Type": "application/json" },
                        body: JSON.stringify({timestep})
                })
        }

	renderEntities(ctx){
		if(!this.newEntities)	return;

		const snapshotInterval = 960; // (self.tick / self.dt) * 1000
		let alpha = (performance.now() - this.lastSnapshotTime) / snapshotInterval;
		alpha = Math.min(alpha, 1);

		ctx.clearRect(0, 0, this.space.screenWidth, this.space.screenHeight); // clear the screen


		//interpolate to simulate frames
		this.newEntities.forEach((newE, i) => { // interpolate each entity and its properties
			const oldE = this.oldEntities?.[i];
        		if (!oldE) {
            			newE.render(ctx, this.space); // the entity
              		        this.properties.renderProperties(ctx, newE, this.space); // its properties
      				return;
        		}
			const interpolatedE = newE.interpolate(oldE, alpha);
                        console.log("interpolatedFrame");
        		interpolatedE.render(ctx, this.space); // the entity
			this.properties.renderProperties(ctx, interpolatedE, this.space); // its properties
		})
	}

	saveData(ctx, data) {
    		const parsed = JSON.parse(data);
                if(this.newEntities){ 	// when a new tick from the phys engine comes in, we save it so that we can simulate FPS by
			this.oldEntities = this.newEntities;   // interpolating between the old and the new state
		}
   		this.newEntities = parsed.entities.map(e => {
       			return new Entity(e.id, e.xPos, e.yPos, e.zPos, e.xVel, e.yVel, e.zVel, e.mass);
    		});
                console.log("snapshot");
		this.lastSnapshotTime = performance.now(); // used to calculate alpha to interpolate the entity
	}

}
