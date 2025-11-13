class Entity:
    def __init__(self, xPos=0, yPos=0, xVel=0, yVel=0, mass=0):
        self.xPos = xPos
        self.yPos = yPos
        self.xVel = xVel
        self.yVel = yVel
        self.mass = mass
        self.xAcc = 0
        self.yAcc = 0

    def update(self, dt=0): # updates the entity based on uniformly accelerated motion formulas
        # s_f = s_0 + v*t + 1/2 a * t^2
        self.xPos += (self.xVel * dt) + (0.5 * self.xAcc * dt * dt)
        self.yPos += (self.yVel * dt) + (0.5 * self.yAcc * dt * dt)

        # v_f = v_0 + a*t
        self.xVel += (self.xAcc * dt)
        self.yVel += (self.yAcc * dt)

    def render(self): # returns a JSON object containing the entity data
        return {
            "xPos": self.xPos,
            "yPos": self.yPos,
            "xVel": self.xVel,
            "yVel": self.yVel,
            "mass": self.mass
        }
