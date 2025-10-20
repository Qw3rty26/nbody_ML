const winWidth = window.innerWidth;
const winHeight = window.innerHeight;

const documentBody = document.getElementById("body");

const documentCanvas = document.getElementById("canvas");
const ctx = documentCanvas.getContext("2d");

documentCanvas.height = winHeight;
documentCanvas.width = winWidth;

const planet = [];
const numEntities = 10;

for (let i = 0; i != numEntities; i++){
	entity[i] = new entity(Math.random() * winWidth, Math.random() * winHeight);
};

function draw () {
	ctx.clearRect(0, 0, documentCanvas.width, documentCanvas.height);
	for(let i = 0; i != numEntities; i++){
		entity[i].render(ctx);
	};
	frame++;
	setTimeout(draw, 1000 / fps); /* limit the fps */
}

let frame = 0;
const fps = 1;
draw();
