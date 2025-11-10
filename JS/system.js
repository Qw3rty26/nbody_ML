class system{
	constructor(numEntities=0, maxX=0, maxY=0){
		this.space = new space(0, 0, maxX, maxY, 100);
		this.properties = new properties();
		this.#initiateSystem(numEntities);
		this.gravity = new gravity();
	}

	addEntity(x=0, y=0, xVel=0, yVel=0,  mass=0){
		this.entity[this.numEntities] = new entity(x, y, xVel, yVel, mass);
                this.numEntities++;
        }

	removeEntity(index){
		for(let i = index + 1; i != this.numEntities; i++){
			this.entity[i - 1] = this.entity[i];
		}
		this.entity[this.numEntities] = [];
		this.numEntities--;
	}


	#initiateSystem(num){
		this.numEntities = 0;
		this.entity = [];
		for(let i = 0; i != num; i++){
			this.addEntity(Math.random() * this.space.screenWidth, Math.random() * this.space.screenHeight, 0, 0, Math.random() * 100);
		}
	}

	render(ctx){
		ctx.clearRect(0, 0, this.space.screenWidth, this.space.screenHeight); // clear the screen
		for(let i = 0; i != this.numEntities; i++){ // cycle through all the entities
			this.entity[i].render(ctx, this.space);
			this.properties.renderProperties(ctx, this.entity[i], this.space);
		}
	}

	#checkCollisions(timeStep = 0, index = 0, recursive = false){
		let hitCheck = false;
		let newTime = 0;
		if(timeStep == 0){
			return 0;
		}
		// collisions logic

		// hit another entity
		// ‖(pA + vA*t) - (pB + vB*t)‖ = rA + rB
		// if(){
		// 	hitCheck = true;
		// }

		// hit the left wall
		// if(){
		// 	hitCheck = true;
		// }

		// hit the right wall
		// if(){
		//	hitCheck = true;
		// }

		// hit the ceiling
		// if(){
		// 	hitCheck = true;
		// }
/*
		// hit the floor
		if(this.entity[index].getRadius() + this.entity[index].getYPos(timeStep) >= this.maxY){
			hitCheck = true;
			// calculate at which fraction of timeStep the collision happens
			
			// Uniformly Accelerated Motion:
			//
			//               ______________________________________________
			//      -v_0 +- V (v_0)^2 - 2 * a * (POSITION + RADIUS - MAXY)
			// t =  -------------------------------------------------------
			//                               a

			let a = this.entity[index].getYAcc();
			let v0 = this.entity[index].getYVel();
			let y0 = this.entity[index].getYPos();
			let r = this.entity[index].getRadius();
			let Ymax = this.maxY;
			let discriminant = v0*v0 - 2*a*(y0 + r - Ymax);
			if (discriminant < 0) return; // no real solution
			let t1 = (-v0 + Math.sqrt(discriminant)) / a;
			let t2 = (-v0 - Math.sqrt(discriminant)) / a;
			if(t1 >= 0 && t2 >= 0){
				newTime = Math.min(t1, t2); // future time
			}else{
				newTime = Math.max(t1, t2); // future time
			}
			this.entity[index].update(newTime); // simulate till floor
			newTime = timeStep - newTime;
			this.entity[index].hitY(); // invert direction
		}else{
			if(recursive == false){
				this.entity[index].removeAcc("normal"); //remove normal force
			}
		}
*/
		if(hitCheck){ // check for a collision within the same timeStep
			return this.#checkCollisions(newTime, index, true); // recursive for multiple collisions within the same timeStep
		}else{
			return timeStep;
		}
	}

	update(timeStep = 0){
		if(timeStep <= 0){
			return;
		}
		this.gravity.naiveCalculate(this.numEntities, this.entity);
		for(let i = 0; i != this.numEntities; i++){
			let entityTimeStep = timeStep;
			entityTimeStep = this.#checkCollisions(entityTimeStep, i, false);
			this.entity[i].update(entityTimeStep);
		}
	}

}
