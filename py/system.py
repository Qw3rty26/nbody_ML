import entity

class System:
    def __init__(self):
        #self.space =
        self.entity = []


    def update(self, timestep=0): # updates entities based on the timestep given
        if timestep <= 0:
            return
        for e in self.entity:
            e.update(timestep)

    def render(self): # returns a JSON object containing an array of entities' data
        return {
            "entities": [e.render() for e in self.entity]
        }

    def addEntity(self, x=0, y=0, xVel=0, yVel=0, mass=0): # adds a new entity
        newEntity = entity.Entity(x, y, xVel, yVel, mass)
        self.entity.append(newEntity)

    def removeEntity(self, entity):
        if entity in self.entity:
            self.entity.remove(entity)

    def clear(self):
        self.entity.clear() 
