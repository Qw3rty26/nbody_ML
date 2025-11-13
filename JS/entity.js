class Entity{	
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
		ctx.lineTo(x + this.xVel * space.scale * 10, y + this.yVel * space.scale * 10);
		ctx.strokeStyle = "red";
		ctx.lineWidth = 2;
		ctx.stroke();
	}

	renderAccelerationVector(ctx, space) {
		const {x, y} = space.toScreen(this.xPos, this.yPos);
		for(let acc of this.Acc.accelerations){
			ctx.beginPath();
			ctx.moveTo(x, y);
			ctx.lineTo(x + acc.x * space.scale * 200, y + acc.y * space.scale * 200);
			ctx.strokeStyle = "green";
			ctx.lineWidth = 2;
			ctx.stroke();

			ctx.fillStyle = "green";
        		ctx.font = "10px Arial";
        		ctx.fillText(acc.type, x + acc.x * space.scale * 2, y + acc.y * space.scale * 2);
		}
	}

}
