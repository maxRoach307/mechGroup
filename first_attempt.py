import numpy as np
import tkinter as tk
import math

class Projectile:
    def __init__(self,Mass,V_x, V_y, x, y, R) -> None:
        self.Mass = Mass
        self.V_X = V_x
        self.V_Y = V_y
        self.X = x
        self.Y = y
        self.R = R

    def getR(self):
        return self.R
    def getX(self):
        return(self.X)
    def getY(self):
        return(self.Y)
    def getV_X(self):
        return(self.V_X)
    def getV_Y(self):
        return(self.V_Y)
    def getSpeed(self):
        return((self.V_X**2 + self.V_Y**2)**(1/2))
    def getEnergy(self):
        return(self.Mass*self.getSpeed()**2)

    def update1(self,F_X,F_Y,dt):
        """Updates the velocity for the given force and then changes its position"""
        self.V_X = self.V_X + (F_X/self.Mass)*dt
        self.V_Y = self.V_Y + (F_Y/self.Mass)*dt
        self.X = self.X + self.V_X*dt
        self.Y = self.Y + self.V_Y*dt
        
    def update(self, dt):
        """Updates the velocity for the given force and then changes its position"""
        self.Y = self.Y + self.V_Y*dt
        self.X = self.X + self.V_X*dt
       
    def Y_pos_at_X(self, x):
        """Returns the lowest point of the projectile at a given x.
        Returns equilibrium position of springs if the projectile is not present here"""
        return (self.getY()-np.sqrt(self.R**2-(x-self.getX())**2))
   
class Spring:
    def __init__(self, x, y, k, m) -> None:
        self.X = x
        self.Y = y
        self.k = k
        self.X_Equ = x
        self.Y_Equ = y
        self.V_X = 0
        self.V_Y = 0
        self.m = m

    def getX(self):
        return self.X
    def getY(self):
        return self.Y
    def getX_EQU(self):
        return self.X_Equ
    def getY_EQU(self):
        return self.Y_Equ
    def getk(self):
        return self.k
    def getV_X(self):
        return self.V_X
    def getV_Y(self):
        return self.V_Y
    def getM(self):
        return self.m
        
    def update(self, dt):
        """Inertial implementation of spring motion"""
        self.V_X = self.V_X + (self.k*((self.X_Equ - self.X))/self.m)*dt
        self.V_Y = self.V_Y + (self.k*((self.Y_Equ - self.Y))/self.m)*dt
        self.X = self.X + self.V_X*dt
        self.Y = self.Y + self.V_Y*dt
        
# =======================================================
# Functions
# =======================================================

def make_node_Array(N_per_row, N_rows, dx, dy, k, m):
    """Takes desired number of springs per row, number of rows, dx, dy, and spring constant
    Returns array containing desired springs"""
    oupt = []
    for i in range(N_rows):
        row = []
        for j in range(N_per_row):
            row.append(Spring(dx*j, dy*i, k, m))
        oupt.append(row)
    return(oupt)
    
def is_touching(spring, projectile):
    """Returns True if a given spring is touching the projectile"""
    # Might make another implementation of this where it just checks if it is beneath the particle and the particle is beneath the equiilbrium point of the springs
    return projectile.Y_pos_at_X(spring.getX()) <= spring.getY_EQU()
    # return projectile.getR() >= math.sqrt((projectile.getX()-spring.getX())**2+(projectile.getY()-spring.getY())**2)
    
def is_touching_Any(springs, projectile):
    """Takes the array of springs and the projectile.
    Returns a True if it is touching any spring in the array, False otherwise"""
    for row in springs:
        for spring in row:
            if (is_touching(spring, projectile)):
                return(True)
    return(False)
    
def add_forces(springs, projectile):
    """Takes an array of springs and a projectile
    Returns the added forces of springs touching the projectile"""
    #This can probably be made to run faster if we check only for springs within R of the projectile, might implement later
    force = 0
    for row in springs:
        for spring in row:
            if is_touching(spring, projectile):
                force = force + spring.getk()*(np.absolute(spring.getY_EQU() - spring.getY()))
    print("Force: ", force)
    return force

def push_outside(spring, projectile):
    """"push the particle to the side of Projectile, set velocity to 0, and handle collision"""
    projectile.V_Y = (spring.m*spring.V_Y+projectile.Mass*projectile.V_Y)/projectile.Mass
    spring.Y = projectile.Y_pos_at_X(spring.getX())
    print("spring velocity: " + str(spring.V_Y))
    print("spring position: ", spring.Y)
    spring.V_Y = 0

# ==============================================================
# Drawing and testing tools
# ==============================================================

def draw_circle(canvas, x, y, radius, color="black"):
    """Takes canvas, an x and y coordinate, radius, and can take a color, default is black
    Side effect, draws a circle using given parameters, and returns this circle"""
    return canvas.create_oval(x-radius, y-radius, x+radius, y+radius, fill=color)

def draw_frame(springs, projectile, spr_size = 0.1, spr_clr = "blue", proj_clr = "red", canvas=None, scale=50, margins=1):
    """Takes springs array and projectile, and can take spr_size, spr_clr, prj_clr, and a pre-made canvas, if none is given, auto-draws one of appropriate dimensions, scale=10, margins=10"""
    if canvas == None:
        win = tk.Tk()
        win.geometry("700x700")

        h = scale*(projectile.getY()+projectile.getR()-springs[0][0].getY())+margins
        w = scale*(springs[0][-1].getX()-springs[0][0].getX())+2*margins

        canvas = tk.Canvas(win, width=w*scale, height=h*scale)
        canvas.pack()

    for row in springs:
        for spring in row:
            draw_circle(canvas, spring.getX()*scale+margins, spring.getY()*scale+margins, spr_size*scale, spr_clr)
    
    draw_circle(canvas, projectile.getX()*scale+margins, projectile.getY()*scale+margins, projectile.getR()*scale, proj_clr)

    win.wait_window(win)

#_________________________________________________________________________________________________________
def main():
    N_per_row = 30
    N_row = 1
    dx = 0.3
    dy = 1
    k = 0.1
    M = 1
    m_spring = 1
    V_X = 0
    V_Y = -0.1
    X = 5
    Y = 3
    R = 1
    dt = 0.1
    timesteps = 300
    show_frame_timer = 100
    f = 0

    springs = make_node_Array(N_per_row, N_row, dx, dy, k, m_spring)
    projectile = Projectile(M, V_X, V_Y, X, Y, R)

    print(projectile.getEnergy())
    draw_frame(springs, projectile)

    n=0
    has_touched = False


    # while(is_touching_All(springs, projectile) or not has_touched):
    for i in range(timesteps):
        F = 0
        # Handle spring motion due to its inertia
        for row in springs:
            for spring in row:
                spring.update(dt)
                # Handle spring collision with projectile
                if is_touching(spring, projectile):
                    # Move spring outside projectile, set v to 0
                    push_outside(spring, projectile)
        projectile.update(dt)
        # if(is_touching_All(springs, projectile)):
        #     print("touching")
        #     has_touched = True
        #     for row in springs:
        #         for spring in row:
        #             if is_touching(spring, projectile):
        #                 n = n + 1
        #                 spring.update()
        #                 print("Spring ", n, " y position: ", spring.getY())
        #     n = 0
        #     F = add_forces(springs, projectile)

        # Handle projectile motion
        print("Energy: ", projectile.getEnergy())
        # projectile.update(0, F, dt)
        print("Y position: ", projectile.getY())
        print("velocity: ", projectile.getV_Y())
        print("----------------------------------------------------------")
        if f % show_frame_timer == 0:
            draw_frame(springs, projectile)
        f = f + 1
    print("Final energy:\n", projectile.getEnergy())
    for row in springs:
        for spring in row:
            print("spring position: ", spring.Y)

    draw_frame(springs, projectile)

main()