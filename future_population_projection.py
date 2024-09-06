import numpy as np
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

# Historical population data (in millions) for the countries
historical_population_data = {
    "Brazil": {
        "years": np.array([1800, 1850, 1900, 1950, 2000, 2023]),
        "population": np.array([4.5, 9.1, 17.4, 51.9, 174.4, 215.3])  # in millions
    },
    "Poland": {
        "years": np.array([1800, 1850, 1900, 1950, 2000, 2023]),
        "population": np.array([7.3, 9.2, 20.0, 25.0, 38.6, 38.0])  # in millions
    },
    "Sweden": {
        "years": np.array([1800, 1850, 1900, 1950, 2000, 2023]),
        "population": np.array([2.3, 3.5, 5.1, 7.0, 8.9, 10.6])  # in millions
    },
    "Italy": {
        "years": np.array([1800, 1850, 1900, 1950, 2000, 2023]),
        "population": np.array([17.3, 24.7, 33.2, 47.1, 57.3, 59.0])  # in millions
    },
    "USA": {
        "years": np.array([1800, 1850, 1900, 1950, 2000, 2023]),
        "population": np.array([5.3, 23.1, 76.2, 151.3, 282.2, 336.0])  # in millions
    },
    "China": {
        "years": np.array([1800, 1850, 1900, 1950, 2000, 2023]),
        "population": np.array([381.0, 430.0, 400.0, 544.0, 1267.4, 1412.0])  # in millions
    },
    "India": {
        "years": np.array([1800, 1850, 1900, 1950, 2000, 2023]),
        "population": np.array([169.0, 208.0, 238.0, 376.3, 1053.6, 1420.0])  # in millions
    }
}

# Logistic growth model for population projection
def logistic_growth(t, P0, r, K):
    """
    Logistic growth model function.
    :param t: time (years)
    :param P0: initial population (at t=0)
    :param r: growth rate
    :param K: carrying capacity (maximum population)
    :return: population at time t
    """
    return K / (1 + ((K - P0) / P0) * np.exp(-r * t))

# Streamlit UI
st.title("Future Population Projection by Country")

# Select country
country = st.selectbox('Select a Country', list(historical_population_data.keys()))

# Define a range of years for projection
years_future = np.arange(2023, 2101, 5)  # future years from 2023 to 2100

# Get historical data for the selected country
data = historical_population_data[country]
years = data['years']
population = data['population']

# Fit the logistic model to the historical data
popt, _ = curve_fit(logistic_growth, years - years[0], population, bounds=(0, [max(population), 0.05, 1.5 * max(population)]))

# Project the future population using the fitted model
future_population = logistic_growth(years_future - years[0], *popt)

# Plot the historical and projected population
fig, ax = plt.subplots()
ax.plot(years, population, 'o', label='Historical Population', markersize=8)
ax.plot(years_future, future_population, '-', label='Projected Population', color='green')
ax.set_xlabel('Year')
ax.set_ylabel('Population (millions)')
ax.set_title(f'Population Projection for {country}')
ax.legend()

# Streamlit output
st.pyplot(fig)

# Display projected population for 2100
st.write(f"Projected population of {country} in 2100: {future_population[-1]:.2f} million people.")