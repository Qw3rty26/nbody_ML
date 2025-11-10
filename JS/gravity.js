class gravity{

	constructor(){
		this.G = 6.6743e-11; // gravitational constant
	}
	
	#getDistance(entity1, entity2){
		let dx = entity2.xPos - entity1.xPos;
		let dy = entity2.yPos - entity1.yPos;
		return Math.sqrt(dx*dx + dy*dy);
	}



	naiveCalculate(numEntities, entityArray){
		for(let i=0; i<numEntities; i++){
			entityArray[i].Acc.deleteAcceleration("gravity");
		}
		
		//calculate gravity accelerations

		for(let i=0; i<numEntities; i++){
			for(let j=i+1; j<numEntities; j++){
				const dx = entityArray[j].xPos - entityArray[i].xPos;
				const dy = entityArray[j].yPos - entityArray[i].yPos;
				const r = Math.sqrt(dx*dx + dy*dy + 1);
				
				if(r === 0) continue;

				let factor = this.G * entityArray[j].mass / (r*r);
				let ax = factor * dx / r;
				let ay = factor * dy / r;

				entityArray[i].Acc.newAcceleration(ax, ay, "gravity");

				factor = this.G * entityArray[i].mass / (r*r);
				ax = -factor * dx / r;
				ay = -factor * dy / r;

				entityArray[j].Acc.newAcceleration(ax, ay, "gravity");
			}
		}

		return;

	}

}
