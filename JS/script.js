let winWidth = window.innerWidth;
let winHeight = window.innerHeight;

const documentBody = document.getElementById("body");


// system containing entities
const systemCanvas = document.getElementById("canvas");
const systemCtx = systemCanvas.getContext("2d");
const rect = systemCanvas.getBoundingClientRect(); // used for mouse position


// background grid
const gridCanvas = document.getElementById("gridCanvas");
const gridCtx = gridCanvas.getContext("2d");


// set canvas resolution 
const dpr = window.devicePixelRatio || 1; // get device pixel ratio
function setCanvasSize(canvas, winWidth, winHeight){
	canvas.width = winWidth * dpr;
	canvas.height = winHeight * dpr;
	canvas.style.width = winWidth + "px";
	canvas.style.height = winHeight + "px";
	canvas.getContext("2d").setTransform(dpr, 0, 0, dpr, 0, 0); // resize canvas to new res
}

setCanvasSize(systemCanvas, winWidth, winHeight);
setCanvasSize(gridCanvas, winWidth, winHeight);

let entitySystem = new system(0, winWidth, winHeight);


entitySystem.addEntity(900, 900, 0, 0, 300);
entitySystem.addEntity(1500, 900, -10, 20, 50);

let initialMouseX = 0;
let initialMouseY = 0;
let isDragging = false;

systemCanvas.addEventListener("mousedown", (event)=>{ // used to drag the space
	//TODO Implement camera following an entity
	event.preventDefault(); // remove default handlers
	isDragging = true;
	initialMouseX = event.clientX - rect.left;
        initialMouseY = event.clientY - rect.top;
})

systemCanvas.addEventListener("mousemove", (event)=>{ // used to drag the space
	event.preventDefault(); // remove default handlers
	if(isDragging){
		let finalMouseX = event.clientX - rect.left;
        	let finalMouseY = event.clientY - rect.top;

        	let draggedX = finalMouseX - initialMouseX;
        	let draggedY = finalMouseY - initialMouseY;

        	entitySystem.space.dragSpace(gridCtx, draggedX, draggedY); // redraw the grid
		entitySystem.render(systemCtx); // render the system

        	initialMouseX = finalMouseX;
        	initialMouseY = finalMouseY;
	}
})

systemCanvas.addEventListener("mouseup", (event)=>{ // used to drag the space
	isDragging = false;
})

systemCanvas.addEventListener("wheel", (event)=>{ // used to zoom in and out
	event.preventDefault(); // remove default handlers
	entitySystem.space.zoomSpace(gridCtx, event.deltaY); // redraw the grid
	entitySystem.render(systemCtx); // render the system
})


//TODO make render and update independent from each other
function render (timeStep) {
	entitySystem.render(systemCtx);
	entitySystem.update(timeStep);
}

function draw () {
	render(time);
	setTimeout(draw, 1000 / fps); // limit the fps 
}

document.addEventListener("DOMContentLoaded", () =>{
	entitySystem.space.dragSpace(gridCtx, 0, 0);
	draw();
})

window.addEventListener("resize", (event)=>{
	winWidth = window.innerWidth;
	winHeight = window.innerHeight;
	
	entitySystem.space.screenWidth = window.innerWidth;
	entitySystem.space.screenHeight = window.innerHeight;
	
	setCanvasSize(gridCanvas, winWidth, winHeight);
	setCanvasSize(systemCanvas, winWidth, winHeight);

        entitySystem.space.dragSpace(gridCtx, 0, 0); // redraw the grid
	entitySystem.render(systemCtx); // render system
})

