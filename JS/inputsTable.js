const velocityCheckbox = document.getElementById("velocityCheckbox");

function setVelocityVectors (bool) {
	entitySystem.properties.velVector = bool;
}

velocityCheckbox.addEventListener("change", () => {
	setVelocityVectors(velocityCheckbox.checked);
});


// initiate velocity vectors
document.addEventListener("DOMContentLoaded", () =>{
	setVelocityVectors(velocityCheckbox.checked);
})


const halfmassradiusCheckbox = document.getElementById("halfmassradiusCheckbox");

function setHalfMassRadius (bool) {
        entitySystem.properties.halfMassRadius = bool;
}

halfmassradiusCheckbox.addEventListener("change", () => {
        setHalfMassRadius(halfmassradiusCheckbox.checked);
});


// initiate velocity vectors
document.addEventListener("DOMContentLoaded", () =>{
        setHalfMassRadius(halfmassradiusCheckbox.checked);
})



/*
const timeSlider = document.getElementById("timeSlider");
const timeSelector = document.getElementById("timeSelector");

let time;

timeSlider.oninput = function () {
	timeSelector.value = this.value;
	setTime(this.value);
}

timeSelector.oninput = function () {
	timeSlider.value = this.value;
	setTime(this.value);
}


const timeStep = document.getElementById("timeStep");
function setTime (value) {
	time = value;
	if(value == 0){
		entitySystem.pauseSSE()
		timeStep.classList.remove("hidden");
	}else{
		timeStep.classList.add("hidden");
	}
}

const stepTimeButton = document.getElementById("stepTimeButton");
const stepTimeSelector = document.getElementById("stepTimeSelector");
stepTimeButton.onclick = function () {
	renderOnce(stepTimeSelector.value);
}

// initiate time
document.addEventListener("DOMContentLoaded", () =>{
	setTime(timeSlider.value);
})




// FPS SLIDER

const fpsSlider = document.getElementById("fpsSlider");
const fpsSelector = document.getElementById("fpsSelector");

let fps = 60; // default value

fpsSlider.oninput = function () {
        fpsSelector.value = this.value;
        setFPS(this.value);
}

fpsSelector.oninput = function () {
        fpsSlider.value = this.value;
        setFPS(this.value);
}


function setFPS (value) {
        fps = value;
}

// initiate time
document.addEventListener("DOMContentLoaded", () =>{
        setFPS(fpsSlider.value);
})
*/
