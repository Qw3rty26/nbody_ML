class System{
	constructor(maxX=0, maxY=0){
		this.space = new space(0, 0, maxX, maxY, 100);
		this.properties = new properties();
		this.newEntities = [];
                this.oldEntities = [];
		this.lastSnapshotTime = performance.now();

		this.sse = null;
		window.addEventListener("beforeunload", () => {
        		if (this.sse) {
            			this.sse.close();
        		}
    		});
	}
	createPhysicsLoop(){
                fetch("http://127.0.0.1:8000/simulation/createPhysicsLoop", {
                        method: "GET",
                        headers: { "Content-Type": "application/json" },
                })
                .then(response => {
                        if (!response.ok) throw new Error("Request failed");
                        this.startPhysicsLoop();
                })
                .catch(err => {
                        console.error("Error creating the physics loop:", err);
                });
        }

	destroyPhysicsLoop(){
                fetch("http://127.0.0.1:8000/simulation/destroyPhysicsLoop", {
                        method: "GET",
                        headers: { "Content-Type": "application/json" },
                })
                .then(response => {
                        if (!response.ok) throw new Error("Request failed");
                        return response.json();
                })
                .catch(err => {
                        console.error("Error destroying the physics loop:", err);
                });
        }

	startPhysicsLoop(){
                fetch("http://127.0.0.1:8000/simulation/startPhysicsLoop", {
                        method: "GET",
                        headers: { "Content-Type": "application/json" },
                })
                .then(response => {
                        if (!response.ok) throw new Error("Request failed");
                        //this.addEntity(0, 0, 0, 0, 0, 0, 1000);
			//this.addEntity(100,0, 0, 0.0, 3.2, 0, 1);

                })
                .catch(err => {
                        console.error("Error starting the physics loop:", err);
                });
        }

	pausePhysicsLoop(){
                fetch("http://127.0.0.1:8000/simulation/pausePhysicsLoop", {
                        method: "GET",
                        headers: { "Content-Type": "application/json" },
                })
                .then(response => {
                        if (!response.ok) throw new Error("Request failed");
                        return response.json();
                })
                .catch(err => {
                        console.error("Error pausing the physics loop:", err);
                });
        }

        connectSSE(){
		// establish SSE connection to stream entity data
        	this.sse = new EventSource("/networking/connectSSE");

        	this.sse.onmessage = (message) => { // SSE packet received
			try {
        			const parsed = JSON.parse(message.data);
        			this.saveData(systemCtx, parsed);
    			}catch (e) {
        			return;
    			}
		};

        	this.sse.onerror = (err) => { // SSE packet not received
                	console.log("SSE error", err);
        	}

		this.sse.onopen = () => {
    			this.createPhysicsLoop();
		};
	}

	disconnectSSE(){
        	fetch("http://127.0.0.1:8000/networking/disconnectSSE", {
                	method: "GET",
                	headers: { "Content-Type": "application/json" },
        	})
        	.then(response => {
                	if (!response.ok) throw new Error("Request failed");
                	return response.json();
        	})
        	.then(data => {
                	this.sse = null;
        	})
        	.catch(err => {
        	        console.error("Error disconnecting SSE:", err);
        	});
	}

	clearSystem(){
		fetch("http://127.0.0.1:8000/simulation/clearSystem", {
                        method: "GET",
                        headers: { "Content-Type": "application/json" },
                })
                .then(response => {
                        if (!response.ok) throw new Error("Request failed");
                        return response.json();
                })
                .catch(err => {
                        console.error("Error in clearing the system:", err);
                });
	}

	addEntity(xPos=0, yPos=0, zPos=0, xVel=0, yVel=0, zVel=0, mass=0){
		fetch("http://127.0.0.1:8000/simulation/addEntity", {
                        method: "POST",
                        headers: { "Content-Type": "application/json" },
                        body: JSON.stringify({xPos, yPos, zPos, xVel, yVel, zVel, mass})
                })
		.then(response => {
                        if (!response.ok) throw new Error("Request failed");
                        return response.json();
                })
                .catch(err => {
                        console.error("Error in adding an entity in the system:", err);
                });
        }

	removeEntity(index){
		fetch("http://127.0.0.1:8000/simulation/removeEntity", {
                        method: "POST",
                        headers: { "Content-Type": "application/json" },
                        body: JSON.stringify({id})
                })
                .then(response => {
                        if (!response.ok) throw new Error("Request failed");
                        return response.json();
                })
                .catch(err => {
                        console.error("Error in removing an entity from the system:", err);
                });
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
                        //console.log("interpolatedFrame");
        		interpolatedE.render(ctx, this.space); // the entity
			this.properties.renderProperties(ctx, interpolatedE, this.space); // its properties
		})
	}

	saveData(ctx, parsed) {
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
