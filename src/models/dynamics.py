def simulate_population_dynamics(population, church_influence, state_power, resources, repression_level, timesteps):
    # Initialize records to store the dynamics over time
    records = []

    for t in range(timesteps):
        # Calculate production based on current population and state power
        production = population * state_power
        resources += production

        # Apply repression effects
        if repression_level > 0:
            resources -= repression_level * resources * 0.1  # Cost of repression

        # Update population dynamics (births and deaths)
        births = int(population * 0.0025)  # Birth rate
        deaths = int(population * 0.0018)   # Death rate
        population += births - deaths

        # Update church influence and state power based on legitimacy
        legitimacy = (church_influence * (population / 10000)) - (repression_level * 0.05)
        state_power += legitimacy * 0.01  # State power grows with legitimacy

        # Record the current state
        records.append({
            'timestep': t,
            'population': population,
            'resources': resources,
            'state_power': state_power,
            'church_influence': church_influence,
            'repression_level': repression_level
        })

    return records

def update_church_influence(church_influence, legitimacy, repression_level):
    # Update church influence based on legitimacy and repression
    church_influence += (legitimacy * 0.005) - (repression_level * 0.01)
    return max(0, min(1, church_influence))  # Clamp between 0 and 1

def adjust_repression_level(repression_level, liberal_fraction):
    # Adjust repression level based on the fraction of liberals
    if liberal_fraction > 0.45:
        repression_level = min(1.0, repression_level + 0.05)  # Increase repression
    else:
        repression_level = max(0.0, repression_level - 0.02)  # Decrease repression
    return repression_level