// VELOCITY CHECKBOX

const velocityCheckbox = document.getElementById("velocityCheckbox");

function setVelocityVectors (bool) {
	entitySystem.toggleVelocityVectors(bool);
}

velocityCheckbox.addEventListener("change", () => {
	setVelocityVectors(velocityCheckbox.checked);
});

document.addEventListener("DOMContentLoaded", () =>{
	setVelocityVectors(velocityCheckbox.checked);
})




// ACCELERATION CHECKBOX

const accelerationCheckbox = document.getElementById("accelerationCheckbox");

function setAccelerationVectors (bool) {
	entitySystem.toggleAccelerationVectors(bool);
}

accelerationCheckbox.addEventListener("change", () => {
	setAccelerationVectors(accelerationCheckbox.checked);
});

document.addEventListener("DOMContentLoaded", () =>{
	setAccelerationVectors(accelerationCheckbox.checked);
})





// TIME SLIDER AND TIMESTEP

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
		timeStep.classList.remove("hidden");
	}else{
		timeStep.classList.add("hidden");
	}
}

const stepTimeButton = document.getElementById("stepTimeButton");
const stepTimeSelector = document.getElementById("stepTimeSelector");
stepTimeButton.onclick = function () {
	render(stepTimeSelector.value);
}

// initiate time
document.addEventListener("DOMContentLoaded", () =>{
	setTime(timeSlider.value);
})
