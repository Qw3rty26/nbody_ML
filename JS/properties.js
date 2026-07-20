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

	setHalfMassRadius(radius, center_of_mass){
		this.halfMassRadius = radius;
		this.centerOfMass = center_of_mass;
	}

	renderHalfMassRadius(ctx, space){
                if(!this.halfMassRadius) return;
                if(this.halfMassRadiusValue == null) return;
                if(!this.centerOfMass) return;
		console.log("halfradius:", this.halfMassRadiusValue, "com:", this.centerOfMass);

                const cx = this.centerOfMass.x;
                const cy = this.centerOfMass.y;

                const screen = space.toScreen(cx, cy);

                const scale = space.scale || 1;
                const r = this.halfMassRadiusValue * scale;

                ctx.save();
                ctx.beginPath();
                ctx.arc(screen.x, screen.y, r, 0, Math.PI * 2);
                ctx.strokeStyle = "red";
                ctx.lineWidth = 20;
                ctx.stroke();
                ctx.restore();
        }

}
