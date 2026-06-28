class Entity{
	constructor(id = 0, xPos = 0.0, yPos = 0.0, zPos = 0.0, xVel = 0.0, yVel = 0.0, zVel = 0.0, mass = 0.0){
		this.id = id;
                this.xPos = xPos;
		this.yPos = yPos;
                this.zPos = zPos;
		this.xVel = xVel;
		this.yVel = yVel;
                this.zVel = zVel;
		this.Acc = new accelerations();
		this.mass = mass;
		if (this.mass > 0.1) {
    			this.radius = 60;
		} else {
    			const m = this.mass / 3e-6;
    			this.radius = Math.max(4, 4 + Math.cbrt(m) * 5);
		}
	}

	render(ctx, space) {
        	//TODO make it so that whenever the entity is outside the screen, it wont get rendered
		const {x, y} = space.toScreen(this.xPos, this.yPos);
		const newRadius = this.radius * space.scale;
		ctx.save();
		ctx.beginPath();
		ctx.arc(x, y, newRadius, 0, 2 * Math.PI); // draw circonference;
		ctx.fillStyle = "#E6EAF2";
        	ctx.strokeStyle = "#E6EAF2";
		ctx.fill();
        	ctx.stroke();
		ctx.restore();
	};

	interpolate(oldE, alpha) { // interpolates the position of the entity using the old state of the entity "oldE" to simulate fps
		return new Entity(
                        oldE.id,
        		oldE.xPos + (this.xPos - oldE.xPos) * alpha,
        		oldE.yPos + (this.yPos - oldE.yPos) * alpha,
                        oldE.zPos,
        		oldE.xVel + (this.xVel - oldE.xVel) * alpha,
        		oldE.yVel + (this.yVel - oldE.yVel) * alpha,
                        oldE.zVel,
        		this.mass
    		);
	}

	//TODO: TO BE FIXED
	renderMass(ctx, space) {
    		const { x, y } = space.toScreen(this.xPos, this.yPos);
    		const radius = this.radius * space.scale;

    		ctx.save();

    		ctx.fillStyle = "white";
    		ctx.font = "12px Arial";
    		ctx.textAlign = "center";
    		ctx.textBaseline = "middle";

    		ctx.fillText(this.mass, x, y);

    		ctx.restore();
	}

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
