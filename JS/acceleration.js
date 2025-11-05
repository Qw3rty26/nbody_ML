class accelerations{
	constructor(x = 0.0, y = 0.0, type = "default"){
		this.accelerations = [];
		this.newAcceleration(x, y, type);
	}

	newAcceleration(x, y, type) {
    		// check if type already exists
    		if (!this.accelerations.some(acc => acc.type === type)) {
        		//console.log("added " + type);
			this.accelerations.push({ x: x, y: y, type: type });
    		}
    		return;
	}

	deleteAcceleration(type){
		this.accelerations = this.accelerations.filter(acc => acc.type !== type);
		return;
	}

	getAccelerations(){
		return this.accelerations;
	}

	getAcceleration(type = "default") {
    		if (type === "total") {
        		return this.accelerations.reduce((sum, acc) => {
            			sum.x += acc.x;
			        sum.y += acc.y;
            			return sum;
        		}, { x: 0, y: 0 });
    		} else {
        		const acc = this.accelerations.find(acc => acc.type === type);
        		if (acc) {
            			return { x: acc.x, y: acc.y };
        		} else {
            			return { x: 0, y: 0 };
        		}
    		}
	}

}
