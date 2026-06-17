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

entitySystem.addEntity(xPos=0, yPos=0, zPos=0, xVel=0, yVel=0, zVel=0, mass=1000);
entitySystem.addEntity(xPos=100, yPos=0, zPos=0, xVel=0.0, yVel=3.2, zVel=0, mass=1);


function renderOnce(timeStep) {
	entitySystem.updateEntities(timeStep, systemCtx); // update entities based on timeStep value
}

function renderLoop () {
	entitySystem.renderEntities(systemCtx);
	requestAnimationFrame(renderLoop); // continuous loop frames
}

document.addEventListener("DOMContentLoaded", () =>{
        // establish SSE connection to stream entity data
    	window.sse = new EventSource("/simulation/startSSE");

    	window.sse.onmessage = (message) => { // SSE packet received
        	entitySystem.saveData(systemCtx, message.data);
    	};

    	window.sse.onerror = (err) => { // SSE packet not received
        	console.log("SSE error", err);
    	};
	requestAnimationFrame(renderLoop); // start displaying frames
})

window.addEventListener("beforeunload", () => {
	window.sse.close();  // close the SSE connection
});

