const BASE_URL = "http://127.0.0.1:8000"

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

	async HTTPrequest(
		url,
		{
			method = "GET",
			body = null,
			headers = { "Content-Type": "application/json" },
			onSuccess = () => {},
			onError = console.error
		} = {}
	) {
		try {
			const response = await fetch(BASE_URL + url, {
				method,
				headers,
				body: body ? JSON.stringify(body) : null
			});

			if (!response.ok) {
				throw new Error(`HTTP ${response.status}`);
			}
			return await onSuccess(response);
		} catch (err) {
			return onError(err);
		}
	}

	async command(url, options = {}){
		return this.HTTPrequest(
			url,
			{
				onError: err => console.error("An error occured whilst processing the " + url + " command\n", err),
				...options
			}
		)
	}

        connectSSE(ctx){
        	this.sse = new EventSource("/networking/connectSSE");

		this.sse.onopen = () => {
			console.log("SSE connected");
			this.command("/simulation/createPhysicsLoop", {});
		}
		this.sse.onmessage = ({data}) => {
			try {
				const parsed_data = JSON.parse(data);
				//console.log(parsed_data);
				if(parsed_data.entities)
					this.updateSnapshot(ctx, parsed_data);
    			} catch(err) {
				console.log(err);
    			}
		}
		this.sse.onerror = err => console.error(err);
	}

	renderEntities(ctx){
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
        		newE.render(ctx, this.space, oldE, alpha); // the entity
			this.properties.renderProperties(ctx, oldE, this.space); // its properties
		})
		this.properties.renderHalfMassRadius(ctx, this.space);
	}

	updateSnapshot(ctx, parsed) {
                if(this.newEntities){ 	// when a new tick from the phys engine comes in, we save it so that we can simulate FPS by
			this.oldEntities = this.newEntities;   // interpolating between the old and the new state
		}
   		this.newEntities = parsed.entities.map(e => {
       			return new Entity(e.id, e.xPos, e.yPos, e.zPos, e.xVel, e.yVel, e.zVel, e.mass);
    		});
                document.getElementById("entitynumber").innerText = this.newEntities.length;
                document.getElementById("elapsedtime").innerText = parsed.time.toFixed(2);
		document.getElementById("dt_time").innerText = parsed.dt.toExponential(2);
                document.getElementById("integrator").innerText = parsed.integrator;
		document.getElementById("initialenergy").innerText = parsed.initial_energy.toFixed(6);
                document.getElementById("errorenergy").innerText = parsed.error_energy.toFixed(6);
                this.properties.setHalfMassRadius(parsed.half_mass_radius, parsed.center_of_mass);
                this.lastSnapshotTime = performance.now(); // used to calculate alpha to interpolate the entity
	}

}
