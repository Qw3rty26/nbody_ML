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


entitySystem.addEntity(900, 1000, 0, 0, 300);
entitySystem.addEntity(1500, 1000, -10, 20, 50);

function renderOnce(timeStep) {
	entitySystem.updateEntities(timeStep, systemCtx); // update entities based on timeStep value
}

function renderLoop () {
	console.log("poll backend")
	setTimeout(renderLoop, 1000); // every second
}

document.addEventListener("DOMContentLoaded", () =>{
	entitySystem.space.dragSpace(gridCtx, 0, 0);
	entitySystem.startSystem();  // start the simulation
	const es = new EventSource("/simulation/streamSystem");
        es.onmessage = (e) => {
            console.log(e.data);
        };
})
