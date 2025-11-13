from system import System

system = System() 

def update(data):
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

def clear():
    system.clear()
    return {}, "application/json"

def html(filename): #returns an html file
    try:
        with open("../HTML/" + filename, "r", encoding="utf-8") as file:
            return file.read(), "text/html"
    except FileNotFoundError:
        return {"message": filename + "could not be found."}, "application/json"

def css(filename): #returns a css file
    try:
        with open("../CSS/" + filename, "r", encoding="utf-8") as file:
            return file.read(), "text/css"
    except FileNotFoundError:
        return {"message": filename + "could not be found."}, "application/json"

def js(filename): #returns a javascript file
    try:
        with open("../JS/" + filename, "r", encoding="utf-8") as file:
            return file.read(), "application/javascript"
    except FileNotFoundError:
        return {"message": filename + "could not be found."}, "application/json"
