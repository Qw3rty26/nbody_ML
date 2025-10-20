class system{
	constructor(numEntities, maxX, maxY){
		this.maxX = maxX;
		this.maxY = maxY;
		this.#initiateSystem(numEntities);
	}

	addEntity(x=0, y=0){
                this.numEntities++;
                this.entity[this.numEntities - 1] = new entity(x, y, 0, 0, Math.random() * 2 - 1, Math.random() * 2 - 1, 10);
        }


	#initiateSystem(num){
		this.numEntities = 0;
		this.entity = [];
		for(let i = 0; i!=num; i++){
			this.addEntity(Math.random() * this.maxX, Math.random() * this.maxY)
		}
	}

	render(ctx){
		for(let i = 0; i!=this.numEntities; i++){
			this.entity[i].render(ctx);
		}
	}

	update(time){
		for(let i = 0; i != this.numEntities; i++){
			this.entity[i].update(time);
			if(this.entity[i].getXPos() + this.entity[i].getRadius() > this.maxX){
				this.entity[i].setXPos(this.maxX - this.entity[i].getRadius());
				this.entity[i].hitX();
			}
			if(this.entity[i].getXPos() - this.entity[i].getRadius() < 0){
				this.entity[i].setXPos(this.entity[i].getRadius());
				this.entity[i].hitX();
			}
			if(this.entity[i].getYPos() + this.entity[i].getRadius() > this.maxY){
                                this.entity[i].setYPos(this.maxY - this.entity[i].getRadius());
                                this.entity[i].hitY();
                        }
                        if(this.entity[i].getYPos() - this.entity[i].getRadius() < 0){
                                this.entity[i].setYPos(this.entity[i].getRadius());
                                this.entity[i].hitY();
                        }
		}
	}
}
