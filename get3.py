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
    k = 0.1
    M = 10
    m = 1
    V_X = 0
    V_Y = -0.1
    X = 1.4
    Y = 1.5
    R = 1
    dt = 0.01
    timesteps = 10000
    show_frame_timer = 2500
    f = 0
    epsilon = 0.0001
    Force = 0
    
    #arrays that hold values for var1 and var2, and energy data
    global var1Data 
    var1Data = []
    global var2Data
    var2Data = []
    global energyData 
    energyData = []
    
    #var1 is the parameter you want to plot. 
    #start1 is the initial value for var1.
    #end1 is the ending value for var1. 
    #step1 is the step size between points on the plot. 
    #This doesn't graph something including both start and end, only including start. But you change how to define step to include end.
    #var2 is the parameter you're changing to observe var1 at different values of var2. You're not plotting var2.
    
    global var1
    var1 = 'k'
    start1 = 0.01
    end1 = 10
    step1 = 0.5
    
    global var2
    var2 = 'V_Y'
    start2 = -200
    end2 = -1
    step2 = 10
    
    #This is solely for the graph is outputted. var2want is the value of var2 you want for a plot displaying energy lost vs var1
    global var2want 
    var2want = 10.0
    
    
    #Changing the initial value of the choosen var1 to start
    if (var1 == 'dx'):
        dx = start1
    elif(var1 == 'k'):
        k = start1
    elif (var1 == 'M'):
        M = start1
    elif (var1 == 'm'):
        m = start1
    elif (var1 == 'V_X'):
        V_X = start1
    elif (var1 == 'V_Y'):
        V_Y = start1
    elif (var1 == 'M'):
        M = start1
    elif (var1 == 'X'):
        X = start1
    elif (var1 == 'Y'):
        Y = start1
    elif (var1 == 'R'):
        R = start1
        
    #Changing the initial value of the choosen var2 to start2
    if (var2 == 'dx'):
        dx = start2
    elif(var2 == 'k'):
        k = start2
    elif (var2 == 'M'):
        M = start2
    elif (var2 == 'm'):
        m = start2
    elif (var2 == 'V_X'):
        V_X = start2
    elif (var2 == 'V_Y'):
        V_Y = start2
    elif (var2 == 'M'):
        M = start2
    elif (var2 == 'X'):
        X = start2
    elif (var2 == 'Y'):
        Y = start2
    elif (var2 == 'R'):
        R = start2
    
    
    
    #Maybe this is bad but it's hard to access the variable you choose so we can just create x that holds the same value as it. 
    x = start1
    
    while (x <= end1):
        y = start2
        
        if (var2 == 'dx'):
            dx = start2
        elif(var2 == 'k'):
            k = start2
        elif (var2 == 'M'):
            M = start2
        elif (var2 == 'm'):
            m = start2
        elif (var2 == 'V_X'):
            V_X = start2
        elif (var2 == 'V_Y'):
            V_Y = start2
        elif (var2 == 'M'):
            M = start2
        elif (var2 == 'X'):
            X = start2
        elif (var2 == 'Y'):
            Y = start2
        elif (var2 == 'R'):
            R = start2
            
        while(y <= end2):

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
            var1Data.append(np.abs(x))
            var2Data.append(np.abs(y))
            energyData.append(np.abs(total_energy_lost))
            
            
            
            if (var2 == 'dx'):
                dx += step2
            elif(var2 == 'k'):
                k += step2
            elif (var2 == 'M'):
                M += step2
            elif (var2 == 'm'):
                m += step2
            elif (var2 == 'V_X'):
                V_X += step2
            elif (var2 == 'V_Y'):
                V_Y += step2
            elif (var2 == 'M'):
                M += step2
            elif (var2 == 'X'):
                X += step2
            elif (var2 == 'Y'):
                Y += step2
            elif (var2 == 'R'):
                R += step2
                
            y += step2
        
        #Step the chosen parameter for var1
        if (var1 == 'dx'):
            dx += step1
        elif(var1 == 'k'):
            k += step1
        elif (var1 == 'M'):
            M += step1
        elif (var1 == 'm'):
            m += step1
        elif (var1 == 'V_X'):
            V_X += step1
        elif (var1 == 'V_Y'):
            V_Y += step1
        elif (var1 == 'M'):
            M += step1
        elif (var1 == 'X'):
            X += step1
        elif (var1 == 'Y'):
            Y += step1
        elif (var1 == 'R'):
            R += step1
        
        print('{}: done'.format(x))
        time.sleep(1)
        x += step1
        

main()

df = pd.DataFrame(columns=[var1, var2, 'Energy Lost'])

for i in range(len(var1Data)):
    newarr = [var1Data[i], var2Data[i], energyData[i]]
    df.loc[len(df)] = newarr
    


output_file = 'moreData.csv'
df.to_csv(output_file)

#next step is to make it so you can input the var2 you want to be used to get the plot for energy lost vs var1
#This means finding a way to filter only the var2 value you want to create a new df and then use the columns
#of that df to plot the graph. 

filt = (df[var2] == var2want)

df_var2want = df[filt]

var1Data = df_var2want[var1].tolist()
energyData = df_var2want['Energy Lost'].tolist()


#plot
plt.plot(var1Data, energyData)

plt.title("Energy Lost vs." + var1)
plt.xlabel(var1)
plt.ylabel('Energy Lost')

plt.show()