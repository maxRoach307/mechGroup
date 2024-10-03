import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import time
#import animation
from functions import *


def main():
    
    #initial variables
    N_springs = 10
    dx = 0.3
    k = 1.1
    M = 10
    m = 1
    V_X = 0
    V_Y = -2
    X = 1.4
    Y = 1.5
    R = 1
    dt = 0.01
    timesteps = 10000
    show_frame_timer = 2500
    f = 0
    epsilon = 0.0001
    Force = 0
    
    global varData 
    varData = []
    global energyData 
    energyData = []
    
    #var is the parameter you want to plot. 
    #start is the initial value for var.
    #end is the ending value for var. 
    #step is the step size between points on the plot. 
    #This doesn't graph something including both start and end, only including start. But you change how to define step to include end.
    global var 
    var = 'k'
    start = 0.1
    end = 10
    step = 0.5
    
    #Changing the initial value of the choosen var to start
    if (var == 'dx'):
        dx = start
    elif(var == 'k'):
        k = start
    elif (var == 'M'):
        M = start
    elif (var == 'm'):
        m = start
    elif (var == 'V_X'):
        V_X = start
    elif (var == 'V_Y'):
        V_Y = start
    elif (var == 'M'):
        M = start
    elif (var == 'X'):
        X = start
    elif (var == 'Y'):
        Y = start
    elif (var == 'R'):
        R = start
    
    #Maybe this is bad but it's hard to access the variable you choose so we can just create x that holds the same value as it. 
    x = start
    while (x <= end):

        springs = init_springs(N_springs, dx, k, m)
        projectile = Projectile(M,V_X, V_Y, X, Y, R)

        px=[]
        py=[]
        springx = []
        springy = []

        for i in range(timesteps):
            for spring in springs:
                if is_touching(spring, projectile, epsilon):
                    push_outside(spring, projectile,epsilon)
        
            Force = add_forces(springs, projectile, epsilon)
            projectile.update(Force[0], Force[1], dt)
            for spring in springs:
                spring.update(spring.get_F_X(), spring.get_F_Y(), dt)

            px.append(projectile.X)
            py.append(projectile.Y)
            springx.append([spring.X for spring in springs])
            springy.append([spring.Y for spring in springs])

        p_df = pd.DataFrame(np.column_stack([px,py]),columns=["pX","pY"])
        sx_df = pd.DataFrame(springx, columns=[f"{i}_x" for i in range(1,N_springs+1)])
        sy_df = pd.DataFrame(springy, columns=[f"{i}_y" for i in range(1,N_springs+1)])
        data = pd.concat([p_df,sx_df,sy_df],axis=1)
    
        output_filename = 'output.csv'
        data.to_csv(output_filename, index_label="timestep")

        
        
        df = pd.read_csv('output.csv')

        mass = 1.0

        def calculate_kinetic_energy(vx_cols, vy_cols, mass):

            ke = pd.Series(0.0, index=df.index)  

            for vx, vy in zip(vx_cols, vy_cols):

                ke += 0.5 * mass * (df[vx]**2 + df[vy]**2)  

            return ke

        vx_cols = [f'{i}_x' for i in range(1, 11)]  # '1_x', '2_x', ..., '10_x'

        vy_cols = [f'{i}_y' for i in range(1, 11)]  # '1_y', '2_y', ..., '10_y'

        df['kinetic_energy'] = calculate_kinetic_energy(vx_cols, vy_cols, mass)

        df['energy_lost'] = df['kinetic_energy'].shift(1) - df['kinetic_energy']

        total_energy_lost = df['energy_lost'].sum()

        
        #Append the absolute value of plotting parameter and energy lost to separate arrays
        varData.append(np.abs(x))
        energyData.append(np.abs(total_energy_lost))
        
        #Step the chosen parameter
        if (var == 'dx'):
            dx += step
        elif(var == 'k'):
            k += step
        elif (var == 'M'):
            M += step
        elif (var == 'm'):
            m += step
        elif (var == 'V_X'):
            V_X += step
        elif (var == 'V_Y'):
            V_Y += step
        elif (var == 'M'):
            M += step
        elif (var == 'X'):
            X += step
        elif (var == 'Y'):
            Y += step
        elif (var == 'R'):
            R += step
            
        x += step
        

main()


print(varData)
print(energyData)

#plot
plt.plot(varData, energyData)

plt.title("Energy Lost vs." + var)
plt.xlabel(var)
plt.ylabel('Energy Lost')

plt.show()
