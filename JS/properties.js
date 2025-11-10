class properties{
	constructor(velVector=false, accVector=false, mass=false, trail=false){
		this.velVector = velVector;
		this.accVector = accVector;
		this.mass = mass;
		this.trail = trail;
	}
	
	renderProperties(ctx, inputEntity, space){
		if(this.velVector){
			inputEntity.renderVelocityVector(ctx, space);
		}

		if(this.accVector){
			inputEntity.renderAccelerationVector(ctx, space);
		}

		if(this.mass){
			//do nothing
		}

		if(this.trail){
			// do nothing
		}
	}

}
