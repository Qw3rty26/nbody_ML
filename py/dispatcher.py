from system import System
import time

system = System()
base_path = __file__.rsplit("/", 2)[0] #get the base path of application


def create_physics_loop():
        system.create_physics_loop()
        return {}, "application/json"

def destroy_physics_loop():
        system.destroy_physics_loop()
        return {}, "application/json"

def start_physics_loop():
        system.start_physics_loop()
        return {}, "application/json"

def pause_physics_loop():
        system.pause_physics_loop()
        return {}, "application/json"

def connect_sse(handler): #establish an SSE connection to constantly stream data to client-side whenever it is ready
        system.connect_sse(handler)
        return {}, "application/json"

def disconnect_sse():
        system.disconnect_sse()
        return {}, "application/json"

def add_entity(data):
	system.simulation.add_entity(data["xPos"], data["yPos"], data["zPos"], data["xVel"], data["yVel"], data["zVel"], data["mass"])
	return {}, "application/json"

def remove_entity(data):
	system.simulation.remove_entity(data["id"])
	return {}, "application/json"

def clear_system():
        system.simulation.clear()
        return {}, "application/json"

def set_timestep(data):
        system.set_timestep(data["timestep"])
        return {}, "application/json"

def html(filename): #returns an html file
	try:
		with open(base_path + "/HTML/" + filename, "r", encoding="utf-8") as file:
			return file.read(), "text/html"
	except FileNotFoundError:
        	return {"message": filename + " could not be found."}, "application/json"

def css(filename): #returns a css file
	try:
		with open(base_path + "/CSS/" + filename, "r", encoding="utf-8") as file:
			return file.read(), "text/css"
	except FileNotFoundError:
		return {"message": filename + " could not be found."}, "application/json"

def js(filename): #returns a javascript file
	try:
		with open(base_path + "/JS/" + filename, "r", encoding="utf-8") as file:
			return file.read(), "application/javascript"
	except FileNotFoundError:
		return {"message": filename + " could not be found."}, "application/json"
