import time
import streamlit as st
import matplotlib.pyplot as plt

# Function to calculate population evolution for a given country
def estimate_population_ever_lived(country_data):
    total_births = 0
    population_data = {"years": [], "total_births": []}  # Store data for plotting

    # Create a Streamlit placeholder for the plot
    plot_placeholder = st.empty()

    # Get the start year of the data for "since" statement
    start_year = country_data[0]["start"]

    # Loop through each period in the country's historical data
    for period in country_data:
        initial_population = period["initial_population"]
        growth_rate = period["growth_rate"]

        for year in range(period["start"], period["end"] + 1):
            # Apply the growth rate and calculate yearly population
            yearly_population = initial_population * (1 + growth_rate) ** (year - period["start"])

            # Estimate the number of births per year based on a crude birth rate (CBR) assumption
            crude_birth_rate = 30 / 1000  # Example: 30 births per 1,000 people
            yearly_births = yearly_population * crude_birth_rate

            total_births += yearly_births

            # Store the population data for plotting
            population_data["years"].append(year)
            population_data["total_births"].append(total_births)

            # Update the live plot every few years to show the evolution in real time
            if year >= 1900:  # Start plotting for modern years
                fig, ax = plt.subplots()
                ax.plot(population_data["years"], population_data["total_births"], color="blue")
                ax.set_xlabel("Year")
                ax.set_ylabel("Total Births (Millions)")
                ax.set_title(f"Population Births Evolution for the Selected Country")
                ax.grid(True)

                # Update the single plot using the placeholder
                plot_placeholder.pyplot(fig)

                # Add a brief pause to simulate live plotting
                time.sleep(0.1)

    return total_births, start_year

# Country data with comments explaining each country's estimation details
countries_data = {
    "Brazil": [
        {"start": 1500, "end": 1800, "growth_rate": 0.005, "initial_population": 0.5},  # Colonial Brazil
        {"start": 1800, "end": 1900, "growth_rate": 0.01, "initial_population": 5},    # Early Modern Brazil
        {"start": 1900, "end": 2000, "growth_rate": 0.03, "initial_population": 25},   # Modern Era Brazil
        {"start": 2000, "end": 2024, "growth_rate": 0.015, "initial_population": 170}, # 21st Century Brazil
        {"start": 2025, "end": 2050, "growth_rate": 0.004, "initial_population": 215.3},  # Future Brazil projection
    ],
    "Poland": [
        {"start": 1000, "end": 1500, "growth_rate": 0.002, "initial_population": 2},   # Early Poland
        {"start": 1500, "end": 1800, "growth_rate": 0.005, "initial_population": 4},   # Renaissance Poland
        {"start": 1800, "end": 1900, "growth_rate": 0.01, "initial_population": 10},   # Modern Era Poland
        {"start": 1900, "end": 2023, "growth_rate": 0.015, "initial_population": 25},  # 20th and 21st Century Poland
        {"start": 2024, "end": 2050, "growth_rate": 0.005, "initial_population": 40},  # Future Poland projection
    ],
    "USA": [
        {"start": 1600, "end": 1800, "growth_rate": 0.01, "initial_population": 0.5},  # Colonial America
        {"start": 1800, "end": 1900, "growth_rate": 0.02, "initial_population": 5},    # 19th Century USA
        {"start": 1900, "end": 2000, "growth_rate": 0.03, "initial_population": 75},   # 20th Century USA
        {"start": 2000, "end": 2024, "growth_rate": 0.01, "initial_population": 300},  # 21st Century USA
        {"start": 2025, "end": 2050, "growth_rate": 0.008, "initial_population": 340}, # Future USA projection
    ],
    "China": [
        {"start": -2000, "end": 1500, "growth_rate": 0.002, "initial_population": 20}, # Ancient China
        {"start": 1500, "end": 1800, "growth_rate": 0.005, "initial_population": 150}, # Imperial China
        {"start": 1800, "end": 1900, "growth_rate": 0.01, "initial_population": 300},  # Late Qing China
        {"start": 1900, "end": 2023, "growth_rate": 0.015, "initial_population": 400}, # 20th and 21st Century China
        {"start": 2024, "end": 2050, "growth_rate": 0.005, "initial_population": 1400}, # Future China projection
    ],
    "India": [
        {"start": -2000, "end": 1500, "growth_rate": 0.002, "initial_population": 20}, # Ancient India
        {"start": 1500, "end": 1800, "growth_rate": 0.005, "initial_population": 150}, # Mughal Empire
        {"start": 1800, "end": 1900, "growth_rate": 0.01, "initial_population": 300},  # Colonial India
        {"start": 1900, "end": 2023, "growth_rate": 0.015, "initial_population": 400}, # 20th and 21st Century India
        {"start": 2024, "end": 2050, "growth_rate": 0.01, "initial_population": 1400},# Future India projection
    ],
    "Sweden": [
        {"start": 1500, "end": 1800, "growth_rate": 0.003, "initial_population": 1},   # Early Sweden
        {"start": 1800, "end": 1900, "growth_rate": 0.01, "initial_population": 4},    # Modern Sweden
        {"start": 1900, "end": 2000, "growth_rate": 0.02, "initial_population": 7},    # 20th Century Sweden
        {"start": 2000, "end": 2024, "growth_rate": 0.01, "initial_population": 9.8},  # 21st Century Sweden
        {"start": 2025, "end": 2050, "growth_rate": 0.005, "initial_population": 10.67}, # Future Sweden projection
    ]
}

# Comments about each country
comments = {
    "Brazil": "Estimates for Brazil start from 1500 when European colonization began, leading to population growth. Significant growth occurred in the 20th century due to industrialization and immigration.",
    "Poland": "Population estimates for Poland start in 1000, a time of kingdom consolidation. The Renaissance and post-war periods saw growth, with modern estimates reflecting post-World War II recovery.",
    "USA": "Starting from 1600 with early European settlement, the U.S. population grew rapidly due to immigration, industrialization, and westward expansion. The 21st century reflects more stable growth.",
    "China": "China’s population estimates date back to -2000, reflecting its long imperial history and the significant population growth during the Qing Dynasty. Modern projections account for the effects of the one-child policy and current growth.",
    "India": "India's estimates begin in -2000, covering ancient civilizations and the Mughal Empire. Modern population growth reflects post-colonial and 21st-century trends, with projections showing continued expansion.",
    "Sweden": "Sweden’s estimates start in 1500, reflecting its period as a powerful kingdom in Europe. Population growth has been steady, with modern growth driven by high living standards and immigration."
}

# Streamlit UI
st.title("Estimated Population Ever Born in Specific Countries")
country = st.selectbox('Select a Country', list(countries_data.keys()))

# Show the comment for the selected country
st.write(comments[country])

if st.button('Start Counting'):
    country_data = countries_data[country]
    total_people_estimate, start_year = estimate_population_ever_lived(country_data)
    st.success(f"According to our Estimation, {total_people_estimate:.2f} million people have been born in {country} since {start_year}")