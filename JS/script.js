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

let entitySystem = new System(winWidth, winHeight);

function renderOnce(timeStep) {
	entitySystem.updateEntities(timeStep, systemCtx); // update entities based on timeStep value
}

function renderLoop () {
	entitySystem.renderEntities(systemCtx);
	requestAnimationFrame(renderLoop); // continuous loop frames
}

document.getElementById("startSimulationButton").addEventListener("click", () => {
	entitySystem.command("/simulation/startPhysicsLoop", {});
});

document.addEventListener("DOMContentLoaded", () =>{
        entitySystem.space.dragSpace(gridCtx, canvas.width/2, canvas.height/2); // redraw the grid
      	entitySystem.connectSSE(); // establish SSE connection
	requestAnimationFrame(renderLoop); // start displaying frames
})

