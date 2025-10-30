import matplotlib.pyplot as plt
import pandas as pd

def plot_population_fractions(df):
    plt.figure(figsize=(10, 5))
    plt.plot(df['t'], df['M'] / df['M'].sum(), label='Monarchists (fraction)')
    plt.plot(df['t'], df['L'] / df['L'].sum(), label='Liberals (fraction)')
    plt.plot(df['t'], df['U'] / df['U'].sum(), label='Undecided (fraction)')
    plt.title('Population Fractions Over Time')
    plt.xlabel('Timestep')
    plt.ylabel('Fraction of population')
    plt.legend()
    plt.grid(True)
    plt.show()

def plot_resources(df):
    plt.figure(figsize=(10, 4))
    plt.plot(df['t'], df['R'], label='Resources (abstract units)')
    plt.title('Resources Over Time')
    plt.xlabel('Timestep')
    plt.ylabel('Resources')
    plt.grid(True)
    plt.show()

def plot_legitimacy_and_state_capacity(df):
    plt.figure(figsize=(10, 4))
    plt.plot(df['t'], df['legitimacy'], label='Legitimacy')
    plt.plot(df['t'], df['S'], label='State Capacity')
    plt.title('Legitimacy and State Capacity')
    plt.xlabel('Timestep')
    plt.ylabel('Value (0..1)')
    plt.legend()
    plt.grid(True)
    plt.show()