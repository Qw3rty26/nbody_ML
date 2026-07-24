class properties{
	constructor(velVector=false, halfMassRadius=false, mass=false, trail=false){
		this.velVector = velVector;
		this.halfMassRadius = halfMassRadius;
		this.mass = mass;
		this.trail = trail;
		this.halfMassRadiusValue = 0;
		this.centerOfMass = 0;
	}
	renderProperties(ctx, inputEntity, space){
		if(this.velVector){
			inputEntity.renderVelocityVector(ctx, space);
		}

		if(this.mass){
			//do nothing
		}

		if(this.trail){
			// do nothing
		}
	}

	setHalfMassRadius(radius, com){
		this.halfMassRadiusValue = radius;
                this.centerOfMass = com;
	}

	renderHalfMassRadius(ctx, space){
		if(!this.halfMassRadius)	return;
		if(this.halfMassRadiusValue == null) return;
    		if(this.centerOfMass == null) 	return;

    		const cx = this.centerOfMass.x;
    		const cy = this.centerOfMass.y;

    		const center = space.toScreen(cx, cy);

		const edge = space.toScreen(cx + this.halfMassRadiusValue, cy);
		const r = Math.abs(edge.x - center.x);

    		ctx.save();
   		ctx.beginPath();
    		ctx.arc(center.x, center.y, r, 0, Math.PI * 2);
    		ctx.strokeStyle = "red";
   		ctx.lineWidth = 2;
    		ctx.stroke();
    		ctx.restore();
	}

}
