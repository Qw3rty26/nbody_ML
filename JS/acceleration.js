class accelerations{
	constructor(x = 0.0, y = 0.0, type = "default"){
		this.accelerations = [];
	}

	newAcceleration(x, y, type) {
    		// check if type already exists
    		const existing = this.accelerations.find(acc => acc.type === type);
		if (existing) {
    			existing.x += x;
			existing.y += y;
		}else{
			this.accelerations.push({x, y, type});
		}
    		return;
	}

	deleteAcceleration(type){
		this.accelerations = this.accelerations.filter(acc => acc.type !== type);
		return;
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
