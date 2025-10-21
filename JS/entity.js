class entity{	
	constructor(xPos = 10, yPos = 10, xVel = 0, yVel = 0, xAcc = 0, yAcc = 0, mass = 10){
		this.xPos = xPos;
		this.yPos = yPos;
		this.xVel = xVel;
		this.yVel = yVel;
		this.xAcc = xAcc;
		this.yAcc = yAcc;
		this.mass = mass;
		this.radius = mass;
	}

	render(ctx) {
        	ctx.beginPath();
        	ctx.arc(this.xPos, this.yPos, this.radius, 0, 2 * Math.PI);
        	ctx.fillStyle = "black";
        	ctx.strokeStyle = "black";
		ctx.fill();
        	ctx.stroke();
	};

	renderVelocityVector(ctx) {
		ctx.beginPath();
		ctx.moveTo(this.xPos, this.yPos);
		ctx.lineTo(this.xPos + this.xVel * 2, this.yPos + this.yVel * 2);
		ctx.strokeStyle = "red";
		ctx.lineWidth = 2;
		ctx.stroke();
	}

	renderAccelerationVector(ctx) {
		ctx.beginPath();
                ctx.moveTo(this.xPos, this.yPos);
                ctx.lineTo(this.xPos + this.xAcc * 50, this.yPos + this.yAcc * 50);
                ctx.strokeStyle = "green";
                ctx.lineWidth = 2;
                ctx.stroke();
	}

	update(time){
		this.xPos = this.xPos + (this.xVel * time);
		this.yPos = this.yPos + (this.yVel * time);

		this.xVel = this.xVel + (this.xAcc * time);
		this.yVel = this.yVel + (this.yAcc * time);
	}

	getXPos(){
		return this.xPos;
	}

	setXPos(x){
		this.xPos = x;
	}

	getYPos(){
		return this.yPos;
	}

	setYPos(y){
		this.yPos = y;
	}

	getRadius(){
		return this.radius;
	}

	hitX(){
		this.xVel *= -0.7;
		if(Math.abs(this.xVel) < 0.4){
			this.xVel = 0;
		}
	}

	hitY(){
		this.yVel *= -0.7;
		if(Math.abs(this.yVel) < 0.4){
			this.yVel = 0;
		}
	}

}
