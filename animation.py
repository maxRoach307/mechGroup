import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.animation as animation

R = 150

path= 'output.csv'
df = pd.read_csv(path)
fig, ax = plt.subplots()

def update(frame):
    ax.clear()
    for i in range((len(df.axes[1]) - 3)//2): # (len(df.axes[1]) - 3)//2 = number of springs
        a = 3
        px = df.iloc[frame,3 + i]#f'{i + 1}_x']
        py = df.iloc[frame,3 + i + 10]#f'{i + 1}_y']
        ax.scatter(px, py, label=f'Spring {i + 1}')
        ax.annotate(f'{i + 1}', (px, py), textcoords="offset points", xytext=(-5,5), ha='center')
    ax.set_title(f'Frame {frame}')
    px = df.iloc[frame,1]#'pX']
    py = df.iloc[frame,2]#'pY']
    ax.scatter(px, py, color='blue')  # Solid core
    ax.scatter(px, py, color='blue', s=R**2, alpha=0.5)
    ax.legend()
    ax.set_ybound(-1,3)

ani = animation.FuncAnimation(fig, update, frames=range(0,len(df),100), interval=100)

plt.show()

#put damping factor in the srpings to see how springs oscillate. 
#most important is to calculate the energy transfer from the projectile to the springs.
#relationship between displacement and force are not linear, but look at literature about "stresstrain diagrams to nitinol" and try to implement it into the spring constant. NOT LINEAR FN