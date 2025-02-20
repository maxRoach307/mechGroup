import pandas as pd

 

# Load the CSV file

df = pd.read_csv('output.csv')

 

# Assume a constant mass for each particle (for example, mass = 1 unit)

mass = 1.0

 

# Calculate the kinetic energy for each particle at each time step

# This function calculates kinetic energy from velocity components

def calculate_kinetic_energy(vx_cols, vy_cols, mass):

    ke = pd.Series(0.0, index=df.index)  # Initialize kinetic energy

    for vx, vy in zip(vx_cols, vy_cols):

        ke += 0.5 * mass * (df[vx]**2 + df[vy]**2)  # KE = 1/2 * m * (vx^2 + vy^2)

    return ke

 

# List of velocity columns for x and y directions

vx_cols = [f'{i}_x' for i in range(1, 11)]  # '1_x', '2_x', ..., '10_x'

vy_cols = [f'{i}_y' for i in range(1, 11)]  # '1_y', '2_y', ..., '10_y'

 

# Calculate kinetic energy at each timestep

df['kinetic_energy'] = calculate_kinetic_energy(vx_cols, vy_cols, mass)

 

# Calculate the energy lost by finding the difference between consecutive timesteps

df['energy_lost'] = df['kinetic_energy'].shift(1) - df['kinetic_energy']

 

# Fill NaN value for the first row (since there is no previous step)

df['energy_lost'].fillna(0, inplace=True)

 

# Output the total energy lost over the entire simulation

total_energy_lost = df['energy_lost'].sum()

 

print(f'Total Energy Lost: {total_energy_lost} units')

 

# Optionally, save the results back to a new CSV file

df.to_csv('particle_collision_energy_loss_output.csv', index=False)