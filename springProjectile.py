import numpy as np

#Projectile class
class Projectile:
    def __init__(self, mass, x_velocity, y_velocity, x, y, radius):
        self.mass = mass
        self.x_velocity = x_velocity
        self.y_velocity = y_velocity
        self.x = x
        self.y = y
        self.radius = radius
    
    def __repr__(self):
        msg = "| Mass: " + str(self.mass) + "| X_Velocity: " + str(self.x_velocity) + "| Y_Velocity: " + str(self.y_velocity) + "| X: " + str(self.x) + "| Y: " + str(self.y) + "| Radius: " + str(self.radius)
        return msg 
    #simple get statements
    
    def getMass(self):
        return self.mass
    def getX_Velocity(self):
        return self.x_velocity
    def getY_Velocity(self):
        return self.y_velocity
    def getXpos(self):
        return self.x
    def getYpos(self):
        return self.y
    def getRadius(self):
        return self.radius
    
    # "complex" get statements
    
    def getSpeed(self):
        return np.sqrt(self.x_velocity**2 + self.y_velocity**2)
    def getKE(self):
        return 0.5 * self.mass * self.getSpeed()**2
    
    #other functions:

    #Updates the velocity for the given force and then changes its position
    def update(self, force_x, force_y, delta_t):
        self.x_velocity += (force_x / self.mass) * delta_t
        self.y_velocity += (force_y / self.mass) * delta_t

        self.x += (self.x_velocity * delta_t) + (0.5 * (force_x * self.mass) * delta_t)**2
        self.y += (self.y_velocity * delta_t) + (0.5 * (force_y * self.mass) * delta_t)**2
    #Returns the lowest point of the projectile at a given x.
    def Y_pos_at_X(self, x):
        return self.y - np.sqrt(abs(self.radius**2 - (x-self.x)**2))

#Spring class   
class Spring:
    def __init__(self, x, y, spring_constant, mass):
        self.x = x
        self.y = y
        self.spring_constant = spring_constant
        self.mass = mass
        self.x_velocity = 0
        self.y_velocity = 0
    
    def __repr__(self):
        msg = "| Mass: " + str(self.mass) + "| X_Velocity: " + str(self.x_velocity) + "| Y_Velocity: " + str(self.y_velocity) + "| X: " + str(self.x) + "| Y: " + str(self.y) + "| Spring Constant: " + str(self.spring_constant)
        return msg 
    
    #get statements
    def getMass(self):
        return self.mass
    def getX_Velocity(self):
        return self.x_velocity
    def getY_Velocity(self):
        return self.y_velocity
    def getXpos(self):
        return self.x
    def getYpos(self):
        return self.y
    def getSpring_Constant(self):
        return self.spring_constant
    
    #other functions
    #Updates the velocity for the given force and then changes its position
    def update(self, force_x, force_y, delta_t):
        self.x_velocity += (force_x / self.mass) * delta_t
        self.y_velocity += (force_y / self.mass) * delta_t

        self.x += (self.x_velocity * delta_t) + (0.5 * (force_x * self.mass) * delta_t)**2
        self.y += (self.y_velocity * delta_t) + (0.5 * (force_y * self.mass) * delta_t)**2