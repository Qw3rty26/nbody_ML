from system import System
import time

system = System()
base_path = __file__.rsplit("/", 2)[0] #get the base path of application

def startSystem():
	system.start()
	return {}, "application/json"

def pauseSystem():
	system.pause()
	return {}, "application/json"

def clearSystem():
        system.clear()
        return {}, "application/json"

def streamSystem(handler):  #establish an SSE connection to constantly stream data to client-side whenever it is ready
        system.startLoop(handler)

def updateSystem(data):
	system.update(data.get("timestep", 0))
	return {}, "application/json"

def render(): #returns a JSON object with entity data
	return system.render(), "application/json"

def addEntity(data):
	system.addEntity(data["x"], data["y"], data["xVel"], data["yVel"], data["mass"])
	return {}, "application/json"

def removeEntity(data):
	#system.removeEntity(data["x"], data["y"], data["xVel"], data["yVel"], data["mass"])
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
