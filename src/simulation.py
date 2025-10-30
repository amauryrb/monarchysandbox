# Simple interactive political sandbox simulation
# Agent-free compartmental model to explore Church-State dynamics for an aspirational monarchy
# Rules: Three population groups: Monarchists (M), Liberals (L), Undecided (U)
# Variables: Church influence (C), State power (S), Resources (R), Repression level (rep)
# Parameters (top of file) are adjustable to run new scenarios.
# Output: time series plots for population fractions, resources, legitimacy, and state power.

import math
import random
import pandas as pd
import matplotlib.pyplot as plt

# ------------------- Parameters (tweak these) -------------------
TIMESTEPS = 120  # months (~10 years)
POP = 10000  # total population
init_M = 0.15   # initial monarchist fraction
init_L = 0.6    # initial liberal fraction
init_U = 0.25   # initial undecided fraction

# Institutional parameters (0..1)
church_influence = 0.2   # C: persuasive power & reach of Church (0-1)
state_capacity = 0.2     # S: initial state administrative/military capacity (0-1)
economic_prod_per_person = 1.0  # baseline production per person per timestep
external_sanction_severity = 0.0  # 0..1, bigger = more economic drain

# Policy levers: adjust to simulate strategies
propaganda_effect = 0.02      # how effectively the State converts undecided -> monarchists per unit S
church_mission_effect = 0.03  # how effectively Church converts undecided -> monarchists per unit C
repression_base = 0.01        # base repression level (costly)
repression_effect_on_L = 0.04 # rate at which repression converts liberals -> undecided (backlash)
repression_legitimacy_cost = 0.03  # how much legitimacy (support) is lost per repression unit
military_maintenance_cost = 0.002  # fraction of resources per unit of state_capacity to maintain force
conversion_from_economic_pain = 0.01  # how economic hardship pushes undecided toward rebelliousness (liberal)

birth_rate = 0.0025   # per person per timestep
death_rate = 0.0018   # baseline per person per timestep

# Random shocks
shock_prob = 0.02
shock_strength = 0.15  # fraction of resources lost

# ------------------- State initialization -------------------
M = int(POP * init_M)
L = int(POP * init_L)
U = POP - M - L

S = state_capacity  # dynamic state capacity (0..1)
C = church_influence  # dynamic church influence (0..1)
R = POP * economic_prod_per_person  # resources (abstract units)
repression = repression_base  # current repression policy intensity (0..1)

# Storage for results
records = []

for t in range(TIMESTEPS):
    # 1) Economic production and external shocks
    production = (M + L + U) * economic_prod_per_person * (0.8 + 0.4 * (S))  # state capacity helps production somewhat
    # Sanctions reduce production and drain reserves
    sanction_drain = external_sanction_severity * (0.1 * R)
    R += production - sanction_drain
    
    # Random shock (war, drought)
    if random.random() < shock_prob:
        loss = R * shock_strength
        R -= loss
        shock_note = True
    else:
        shock_note = False
    
    # 2) Costs of maintaining state force and repression (reduces resources)
    maintenance = military_maintenance_cost * S * R
    repression_cost = repression * 0.05 * R  # repression is expensive: policing, prisons, etc.
    R -= (maintenance + repression_cost)
    
    # 3) Demographics (simple)
    births = int((M + L + U) * birth_rate)
    deaths = int((M + L + U) * death_rate)
    
    # 4) Conversion dynamics
    # Propaganda and Church mission convert undecided to monarchists (when present)
    conv_prop = int(min(U, propaganda_effect * S * U))
    conv_church = int(min(U - conv_prop, church_mission_effect * C * U))
    # Repression causes backlash: some liberals become undecided or radicalized
    backlash = int(min(L, repression_effect_on_L * repression * L))
    # Economic pain pushes undecided toward liberal / rebellious
    econ_push = int(min(U - conv_prop - conv_church, conversion_from_economic_pain * max(0, (POP*2 - R)/ (POP*2)) * U))
    
    # Apply conversions
    U = U - conv_prop - conv_church - econ_push + backlash  # backlash moves from L -> U; econ_push moves U->L
    M += conv_prop + conv_church
    L += econ_push - backlash
    
    # 5) Legitimacy metric (abstract): combines Church influence, support among population, and cost of repression
    support_fraction = M / (M + L + U)
    legitimacy = C * support_fraction - repression * repression_legitimacy_cost - (external_sanction_severity * 0.2)
    # Clamp legitimacy
    legitimacy = max(-1.0, min(1.0, legitimacy))
    
    # 6) State capacity update: grows with resources and legitimacy, shrinks with low resources and low legitimacy
    S_growth = 0.01 * (R / (POP * economic_prod_per_person)) * max(0, legitimacy + 0.2)
    S = max(0.0, min(1.0, S + S_growth - 0.005 * (1 - legitimacy)))
    
    # 7) Church influence dynamics: grows with public participation (proxy = M fraction), decreases with repression
    C = max(0.0, min(1.0, C + 0.005 * (support_fraction) - 0.01 * repression))
    
    # 8) Repression policy: simple rule - increase repression when insurgent threat (L high) passes threshold; otherwise slowly relax
    if L / (M + L + U) > 0.45:  # if liberals dominate dangerously
        repression = min(1.0, repression + 0.05)
    else:
        repression = max(0.0, repression - 0.02)
    
    # 9) Update population with births/deaths
    total_pop = M + L + U + births - deaths
    # Re-normalize to POP (simulate migration zero-sum)
    if total_pop > 0:
        scale = POP / total_pop
        M = int(M * scale)
        L = int(L * scale)
        U = POP - M - L
    else:
        M = int(POP * 0.1)
        L = int(POP * 0.8)
        U = POP - M - L
    
    # Record timestep
    records.append({
        't': t,
        'M': M,
        'L': L,
        'U': U,
        'S': S,
        'C': C,
        'R': R,
        'repression': repression,
        'legitimacy': legitimacy,
        'shock': shock_note
    })

df = pd.DataFrame(records)

# Display a small table for the final state
final = df.iloc[-1].to_dict()

# Plotting: population fractions, resources, legitimacy, state capacity
plt.figure(figsize=(10,5))
plt.plot(df['t'], df['M'] / POP, label='Monarchists (fraction)')
plt.plot(df['t'], df['L'] / POP, label='Liberals (fraction)')
plt.plot(df['t'], df['U'] / POP, label='Undecided (fraction)')
plt.title('Population Fractions Over Time')
plt.xlabel('Timestep')
plt.ylabel('Fraction of population')
plt.legend()
plt.grid(True)
plt.show()

plt.figure(figsize=(10,4))
plt.plot(df['t'], df['R'], label='Resources (abstract units)')
plt.title('Resources Over Time')
plt.xlabel('Timestep')
plt.ylabel('Resources')
plt.grid(True)
plt.show()

plt.figure(figsize=(10,4))
plt.plot(df['t'], df['legitimacy'], label='Legitimacy')
plt.plot(df['t'], df['S'], label='State Capacity')
plt.title('Legitimacy and State Capacity')
plt.xlabel('Timestep')
plt.ylabel('Value (0..1)')
plt.legend()
plt.grid(True)
plt.show()

# Show final few rows
display_df = df.tail(6)[['t','M','L','U','S','C','R','repression','legitimacy']].copy()
import caas_jupyter_tools as tools; tools.display_dataframe_to_user("Sandbox Simulation - final steps", display_df)

# Print summary
print("Final state after", TIMESTEPS, "timesteps:")
print(f"Monarchists: {final['M']}  Liberals: {final['L']}  Undecided: {final['U']}")
print(f"State capacity (S): {final['S']:.3f}  Church influence (C): {final['C']:.3f}")
print(f"Resources: {final['R']:.1f}  Repression: {final['repression']:.3f}  Legitimacy: {final['legitimacy']:.3f}")

# Save dataframe for potential download
df.to_csv('/mnt/data/sandbox_simulation.csv', index=False)
print("\n[Download the simulation CSV](/mnt/data/sandbox_simulation.csv)")