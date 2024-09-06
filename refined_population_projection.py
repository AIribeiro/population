import numpy as np
import streamlit as st
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

# Historical population data (in millions) for the countries
historical_population_data = {
    "Brazil": {
        "years": np.array([1800, 1850, 1900, 1950, 2000, 2023]),
        "population": np.array([4.5, 9.1, 17.4, 51.9, 174.4, 215.3]),  # in millions
        "birth_rate": 14.2,  # per 1000 people
        "death_rate": 6.7,   # per 1000 people
        "migration_rate": 0.3  # net migration per 1000 people
    },
    "Poland": {
        "years": np.array([1800, 1850, 1900, 1950, 2000, 2023]),
        "population": np.array([7.3, 9.2, 20.0, 25.0, 38.6, 38.0]),  # in millions
        "birth_rate": 9.5,   # per 1000 people
        "death_rate": 10.7,  # per 1000 people
        "migration_rate": -0.4  # net migration per 1000 people
    },
    "Sweden": {
        "years": np.array([1800, 1850, 1900, 1950, 2000, 2023]),
        "population": np.array([2.3, 3.5, 5.1, 7.0, 8.9, 10.6]),  # in millions
        "birth_rate": 11.4,  # per 1000 people
        "death_rate": 9.3,   # per 1000 people
        "migration_rate": 5.3  # net migration per 1000 people
    },
    "Italy": {
        "years": np.array([1800, 1850, 1900, 1950, 2000, 2023]),
        "population": np.array([17.3, 24.7, 33.2, 47.1, 57.3, 59.0]),  # in millions
        "birth_rate": 7.6,   # per 1000 people
        "death_rate": 10.7,  # per 1000 people
        "migration_rate": 2.2  # net migration per 1000 people
    },
    "USA": {
        "years": np.array([1800, 1850, 1900, 1950, 2000, 2023]),
        "population": np.array([5.3, 23.1, 76.2, 151.3, 282.2, 336.0]),  # in millions
        "birth_rate": 12.4,  # per 1000 people
        "death_rate": 8.4,   # per 1000 people
        "migration_rate": 3.0  # net migration per 1000 people
    },
    "China": {
        "years": np.array([1800, 1850, 1900, 1950, 2000, 2023]),
        "population": np.array([381.0, 430.0, 400.0, 544.0, 1267.4, 1412.0]),  # in millions
        "birth_rate": 10.5,  # per 1000 people
        "death_rate": 7.3,   # per 1000 people
        "migration_rate": -0.3  # net migration per 1000 people
    },
    "India": {
        "years": np.array([1800, 1850, 1900, 1950, 2000, 2023]),
        "population": np.array([169.0, 208.0, 238.0, 376.3, 1053.6, 1420.0]),  # in millions
        "birth_rate": 17.4,  # per 1000 people
        "death_rate": 7.3,   # per 1000 people
        "migration_rate": -0.1  # net migration per 1000 people
    }
}

# Logistic growth model function without migration
def logistic_growth(t, P0, r, K):
    """
    Logistic growth model function without migration.
    :param t: time (years)
    :param P0: initial population (at t=0)
    :param r: growth rate
    :param K: carrying capacity (maximum population)
    :return: population at time t
    """
    return K / (1 + ((K - P0) / P0) * np.exp(-r * t))

# Streamlit UI
st.title("Refined Population Projection by Country with Different Scenarios")

# Select country
country = st.selectbox('Select a Country', list(historical_population_data.keys()))

# Get historical data for the selected country
data = historical_population_data[country]
years = data['years']
population = data['population']
birth_rate = data['birth_rate']
death_rate = data['death_rate']
migration_rate = data['migration_rate']
current_population = population[-1]

# Define future scenarios
scenarios = {
    "High Growth": {"r": 0.02, "K": 1.2 * max(population)},  # Faster growth, higher carrying capacity
    "Moderate Growth": {"r": 0.01, "K": max(population)},    # Moderate growth, current carrying capacity
    "Low Growth": {"r": 0.005, "K": 0.8 * max(population)},  # Slower growth, reduced carrying capacity
}

# User selects growth scenario
scenario = st.selectbox("Select a Future Growth Scenario", list(scenarios.keys()))

# Get scenario parameters
growth_rate = scenarios[scenario]['r']
carrying_capacity = scenarios[scenario]['K']

# Define future years for projection
years_future = np.arange(2023, 2101, 5)

# Fit the logistic model to historical data to estimate the initial population (P0)
popt, _ = curve_fit(
    lambda t, P0: logistic_growth(t, P0, growth_rate, carrying_capacity), 
    years - years[0], 
    population, 
    bounds=(0, [max(population)])
)

# Extract fitted initial population (P0)
P0_fitted = popt[0]

# Project the future population using the manually applied scenario parameters
future_population = logistic_growth(years_future - years[0], P0_fitted, growth_rate, carrying_capacity)

# Calculate percentage growth from the current population to the 2100 projection
growth_percentage = ((future_population[-1] - current_population) / current_population) * 100

# Plot the historical and projected population
fig, ax = plt.subplots()
ax.plot(years, population, 'o-', label='Historical Population', markersize=8, color='blue')  # Connect historical population with line
ax.plot(np.append(years[-1], years_future), np.append(population[-1], future_population), '-', label=f'Projected Population ({scenario})', color='green')
ax.set_xlabel('Year')
ax.set_ylabel('Population (millions)')
ax.set_title(f'Population Projection for {country} ({scenario})')
ax.legend()

# Streamlit output
st.pyplot(fig)

# Display projected population for 2100 with more information
st.write(f"Current population of {country}: {current_population:.2f} million people.")
st.write(f"Projected population of {country} in 2100 under {scenario} scenario: {future_population[-1]:.2f} million people.")
st.write(f"Percentage change from 2023 to 2100: {growth_percentage:.2f}%.")