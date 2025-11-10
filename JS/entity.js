class entity{	
	constructor(xPos = 10.0, yPos = 10.0, xVel = 0.0, yVel = 0.0, mass = 10.0){
		this.xPos = xPos;
		this.yPos = yPos;
		this.xVel = xVel;
		this.yVel = yVel;
		this.Acc = new accelerations();
		this.mass = mass * 1e13;
		this.radius = this.mass * 1e-13 ;
	}

	render(ctx, space) {
        	//TODO make it so that whenever the entity is outside the screen, it wont get rendered
		const {x, y} = space.toScreen(this.xPos, this.yPos);
		const radius = this.radius * space.scale;
		ctx.beginPath();
		ctx.arc(x, y, radius, 0, 2 * Math.PI); // draw circonference;
		ctx.fillStyle = "black";
        	ctx.strokeStyle = "black";
		ctx.fill();
        	ctx.stroke();
	};

	renderVelocityVector(ctx, space) {
		const {x, y} = space.toScreen(this.xPos, this.yPos);
		ctx.beginPath();
		ctx.moveTo(x, y);
		ctx.lineTo(x + this.xVel * space.scale * 2, y + this.yVel * space.scale * 2);
		ctx.strokeStyle = "red";
		ctx.lineWidth = 2;
		ctx.stroke();
	}

	renderAccelerationVector(ctx, space) {
		const {x, y} = space.toScreen(this.xPos, this.yPos);
		for(let acc of this.Acc.accelerations){
			ctx.beginPath();
			ctx.moveTo(x, y);
			ctx.lineTo(x + acc.x * space.scale * 10, y + acc.y * space.scale * 10);
			ctx.strokeStyle = "green";
			ctx.lineWidth = 2;
			ctx.stroke();

			ctx.fillStyle = "green";
        		ctx.font = "10px Arial";
        		ctx.fillText(acc.type, x + acc.x * space.scale * 2, y + acc.y * space.scale * 2);
		}
	}

	update(dt = 0){
		let totalAcc = this.Acc.getAcceleration("total");	
		this.xPos = this.xPos + (this.xVel * dt) + 0.5 * totalAcc.x * dt * dt;
		this.yPos = this.yPos + (this.yVel * dt) + 0.5 * totalAcc.y * dt * dt;
		

		this.xVel = this.xVel + (totalAcc.x * dt);
		this.yVel = this.yVel + (totalAcc.y * dt);
		//console.log("xAcc: " + totalAcc.x + " yAcc: " + totalAcc.y);
		//console.log("xVel: " + this.xVel + " yVel: " + this.yVel);
	
	}

	getXPos(timeStep = 0){
		let xPos = this.xPos + (this.xVel * timeStep);
		return xPos;
	}

	getYPos(dt = 0){
		if(dt <= 0){
			return this.yPos;
		}
		let totalAcc = this.Acc.getAcceleration("total");
		let yPos = this.yPos + (this.yVel * dt) + 0.5 * totalAcc.y * dt * dt;
                return yPos;
        }

	getXAcc(){
		let totalAcc = this.Acc.getAcceleration("total");
                return totalAcc.x;
        }

	getYAcc(type = "default"){
		let totalAcc = this.Acc.getAcceleration("total");
                return totalAcc.y;
	}

	hitY(){
		let elasticity = 0.7;
		// apply acceleration given by the normal force coming from the floor
		this.yVel = this.yVel * -1 * elasticity;
		this.Acc.newAcceleration(0, -9.8, "normal");
	}

}
