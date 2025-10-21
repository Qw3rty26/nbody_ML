const winWidth = window.innerWidth;
const winHeight = window.innerHeight;

const documentBody = document.getElementById("body");

const documentCanvas = document.getElementById("canvas");
const ctx = documentCanvas.getContext("2d");
const rect = documentCanvas.getBoundingClientRect();

documentCanvas.height = winHeight;
documentCanvas.width = winWidth;

let entitySystem = new system(2, winWidth, winHeight);

const fps = 60;

documentCanvas.addEventListener("click", (event) => {
	// Calculate mouse coordinates relative to the canvas
	let mouseX = event.clientX - rect.left;
	let mouseY = event.clientY - rect.top;
	entitySystem.addEntity(mouseX, mouseY);
});


function render (timeStep) {
	ctx.clearRect(0, 0, documentCanvas.width, documentCanvas.height); /* clear the screen */
	entitySystem.render(ctx);
	entitySystem.update(timeStep);
}

function draw () {
	render(time);
	setTimeout(draw, 1000 / fps); /* limit the fps */
}

draw();
