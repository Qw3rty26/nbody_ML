class entity{	
	constructor(x, y){
		this.x = x;
		this.y = y;
	}

	render(ctx) {
        	ctx.beginPath();
        	ctx.arc(this.x, this.y, 10, 0, 2 * Math.PI);
        	ctx.fillStyle = "black";
        	ctx.fill();
        	ctx.stroke();
	};
}
