class System{
	constructor(maxX=0, maxY=0){
		this.space = new space(0, 0, maxX, maxY, 100);
		this.properties = new properties();
		this.gravity = new gravity();
		this.entities = [];
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

	addEntity(x=0, y=0, xVel=0, yVel=0,  mass=0){
		fetch("http://127.0.0.1:8000/simulation/add_entity", {
                        method: "POST",
                        headers: { "Content-Type": "application/json" },
                        body: JSON.stringify({x, y, xVel, yVel, mass})
                })
        }

	removeEntity(index){
		//POST fetch
	}

	renderEntities(ctx){
		ctx.clearRect(0, 0, this.space.screenWidth, this.space.screenHeight); // clear the screen
		this.entities.forEach(e =>{ // render each entity and its properties
                	e.render(ctx, this.space); // entity
                       	this.properties.renderProperties(ctx, e, this.space); // its properties
        	})
	}

	displayData(ctx, data) {
    		const parsed = JSON.parse(data);

   		this.entities = parsed.entities.map(e => {
       			return new Entity(e.xPos, e.yPos, e.xVel, e.yVel, e.mass);
    		});
    		this.renderEntities(ctx);
	}

	updateEntities(timeStep = 0, ctx){
		if(timeStep <= 0) return;
		fetch("http://127.0.0.1:8000/simulation/update", {
    			method: "POST",
    			headers: { "Content-Type": "application/json" },
    			body: JSON.stringify({"timestep": Number(timeStep)})
		})
		.then(() => this.fetchEntities(ctx)) // fetch the newly updated entity positions
	}

}
