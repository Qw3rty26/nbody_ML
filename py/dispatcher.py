from system import System
import time

system = System()
base_path = __file__.rsplit("/", 2)[0] #get the base path of application


def createPhysicsLoop():
        system.createPhysicsLoop()
        return {}, "application/json"

def destroyPhysicsLoop():
        system.destroyPhysicsLoop()
        return {}, "application/json"

def startPhysicsLoop():
        system.startPhysicsLoop()
        return {}, "application/json"

def pausePhysicsLoop():
        system.pausePhysicsLoop()
        return {}, "application/json"

def connectSSE(handler): #establish an SSE connection to constantly stream data to client-side whenever it is ready
        system.connectSSE(handler)
        return {}, "application/json"

def disconnectSSE():
        system.disconnectSSE()
        return {}, "application/json"

def addEntity(data):
	system.simulation.addEntity(data["xPos"], data["yPos"], data["zPos"], data["xVel"], data["yVel"], data["zVel"], data["mass"])
	return {}, "application/json"

def removeEntity(data):
	system.simulation.removeEntity(data["id"])
	return {}, "application/json"

def clearSystem():
        system.simulation.clear()
        return {}, "application/json"

def setTimestep(data):
        system.setTimestep(data["timestep"])
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
