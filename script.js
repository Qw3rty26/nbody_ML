const winWidth = window.innerWidth;
const winHeight = window.innerHeight;

const documentBody = document.getElementById("body");

const documentCanvas = document.getElementById("canvas");
const ctx = documentCanvas.getContext("2d");
const rect = documentCanvas.getBoundingClientRect();

documentCanvas.height = winHeight;
documentCanvas.width = winWidth;

const planet = [];
const numEntities = 10;

/*
for (let i = 0; i != numEntities; i++){
	entity[i] = new entity(Math.random() * winWidth, Math.random() * winHeight);
};*/

let entitySystem = new system(5, winWidth, winHeight);

documentCanvas.addEventListener("click", (event) => {
	// Calculate mouse coordinates relative to the canvas
	let mouseX = event.clientX - rect.left;
	let mouseY = event.clientY - rect.top;
	entitySystem.addEntity(mouseX, mouseY);
});


function draw () {
	ctx.clearRect(0, 0, documentCanvas.width, documentCanvas.height);
	/*for(let i = 0; i != numEntities; i++){
		entity[i].render(ctx);
	};*/
	entitySystem.render(ctx);
	entitySystem.update(1);
	frame++;
	setTimeout(draw, 1000 / fps); /* limit the fps */
}

let frame = 0;
const fps = 60;
draw();
