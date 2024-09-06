import time
import numpy as np
import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from scipy.optimize import curve_fit

# -----------------------------------------------
# App 1: Global Population Evolution Based on Updated Data
# -----------------------------------------------
def people_ever_lived():
    # Updated population data from the article
    periods = [
        {"year": 190000, "population": 2, "birth_rate": 80},  # 190,000 BCE
        {"year": 50000, "population": 2_000_000, "birth_rate": 80},  # 50,000 BCE
        {"year": 8000, "population": 5_000_000, "birth_rate": 80},  # 8000 BCE
        {"year": 1, "population": 300_000_000, "birth_rate": 80},  # 1 CE
        {"year": 1200, "population": 450_000_000, "birth_rate": 60},  # 1200 CE
        {"year": 1650, "population": 500_000_000, "birth_rate": 60},  # 1650 CE
        {"year": 1750, "population": 795_000_000, "birth_rate": 50},  # 1750 CE
        {"year": 1850, "population": 1_265_000_000, "birth_rate": 40},  # 1850 CE
        {"year": 1900, "population": 1_656_000_000, "birth_rate": 40},  # 1900 CE
        {"year": 1950, "population": 2_499_000_000, "birth_rate": 31},  # 1950 CE
        {"year": 2000, "population": 6_149_000_000, "birth_rate": 22},  # 2000 CE
        {"year": 2022, "population": 7_963_500_000, "birth_rate": 17},  # 2022 CE
        {"year": 2035, "population": 8_899_000_000, "birth_rate": 16},  # 2035 CE (projection)
        {"year": 2050, "population": 9_752_000_000, "birth_rate": 14},  # 2050 CE (projection)
    ]

    total_people_born = 0  # Total number of people born
    total_people_born_in_billions = 0  # In billions for easier readability
    population_data = {"years": [], "total_population": []}

    for i in range(len(periods) - 1):
        start_year = periods[i]["year"]
        end_year = periods[i + 1]["year"]
        birth_rate = periods[i]["birth_rate"]
        population = periods[i]["population"]

        # Calculate births during this period
        for year in range(start_year, end_year):
            births_this_year = (population * birth_rate) / 1000

            # Cap the population and birth growth to prevent explosion
            population += births_this_year * 0.5  # Adjust population growth realistically
            total_people_born += births_this_year
            total_people_born_in_billions = total_people_born / 1e9  # Convert to billions

            # Store yearly data for plotting
            population_data["years"].append(year)
            population_data["total_population"].append(total_people_born_in_billions)

    return total_people_born_in_billions, population_data

# -----------------------------------------------
# App 2: Country-Specific Population Evolution (using a similar method to update numbers)
# -----------------------------------------------
def estimate_population_ever_lived(country_data):
    total_people = 0
    population_data = {"years": [], "total_population": []}
    plot_placeholder = st.empty()

    for period in country_data:
        initial_population = period["initial_population"]
        growth_rate = period["growth_rate"]

        for year in range(period["start"], period["end"] + 1):
            yearly_population = initial_population * (1 + growth_rate) ** (year - period["start"])
            total_people += yearly_population
            population_data["years"].append(year)
            population_data["total_population"].append(total_people)

            if year >= 1900:
                fig, ax = plt.subplots()
                ax.plot(population_data["years"], population_data["total_population"], color="blue")
                ax.set_xlabel("Year")
                ax.set_ylabel("Total Population (Billions)")
                ax.set_title(f"Population Evolution for the Selected Country")
                ax.grid(True)
                plot_placeholder.pyplot(fig)
                time.sleep(0.1)

    return total_people

# -----------------------------------------------
# App 3: Logistic Growth Model for Population Projection (unchanged)
# -----------------------------------------------
historical_population_data = {
    "Brazil": {
        "years": np.array([1800, 1850, 1900, 1950, 2000, 2020]),
        "population": np.array([4.5, 9.1, 17.4, 51.9, 174.4, 212.6])
    },
    # Add other countries here...
}

def population_projection(country):
    data = historical_population_data[country]
    years = data['years']
    population = data['population']
    years_future = np.arange(2020, 2101, 5)

    def logistic_growth(t, P0, r, K):
        return K / (1 + ((K - P0) / P0) * np.exp(-r * t))

    popt, _ = curve_fit(logistic_growth, years - years[0], population,
                        bounds=(0, [max(population), 0.05, 1.5 * max(population)]))
    future_population = logistic_growth(years_future - years[0], *popt)

    fig, ax = plt.subplots()
    ax.plot(years, population, 'o', label='Historical Population', markersize=8)
    ax.plot(years_future, future_population, '-', label='Projected Population', color='green')
    ax.set_xlabel('Year')
    ax.set_ylabel('Population (millions)')
    ax.set_title(f'Population Projection for {country}')
    ax.legend()
    st.pyplot(fig)
    st.write(f"Projected population of {country} in 2100: {future_population[-1]:.2f} million people.")

# -----------------------------------------------
# App 4: Refined Population Projection with Scenarios (unchanged)
# -----------------------------------------------
refined_population_data = {
    "Brazil": {
        "years": np.array([1800, 1850, 1900, 1950, 2000, 2020]),
        "population": np.array([4.5, 9.1, 17.4, 51.9, 174.4, 212.6]),
        "birth_rate": 14.2,
        "death_rate": 6.7,
        "migration_rate": 0.3
    },
    # Add other countries here...
}

def refined_population_projection(country, scenario):
    data = refined_population_data[country]
    years = data['years']
    population = data['population']
    birth_rate = data['birth_rate']
    death_rate = data['death_rate']
    migration_rate = data['migration_rate']
    years_future = np.arange(2020, 2101, 5)

    scenarios = {
        "High Growth": {"r": 0.02, "K": 1.2 * max(population)},
        "Moderate Growth": {"r": 0.01, "K": max(population)},
        "Low Growth": {"r": 0.005, "K": 0.8 * max(population)}
    }

    def logistic_growth(t, P0, r, K):
        return K / (1 + ((K - P0) / P0) * np.exp(-r * t))

    r = scenarios[scenario]["r"]
    K = scenarios[scenario]["K"]

    popt, _ = curve_fit(lambda t, P0: logistic_growth(t, P0, r, K), years - years[0], population, bounds=(0, [max(population)]))
    P0_fitted = popt[0]
    future_population = logistic_growth(years_future - years[0], P0_fitted, r, K)

    fig, ax = plt.subplots()
    ax.plot(years, population, 'o', label='Historical Population', markersize=8)
    ax.plot(years_future, future_population, '-', label=f'Projected Population ({scenario})', color='green')
    ax.set_xlabel('Year')
    ax.set_ylabel('Population (millions)')
    ax.set_title(f'Population Projection for {country} ({scenario})')
    ax.legend()
    st.pyplot(fig)
    st.write(f"Projected population of {country} in 2100 under {scenario} scenario: {future_population[-1]:.2f} million people.")

# -----------------------------------------------
# Streamlit Main App
# -----------------------------------------------
st.title("Global and Country-Specific Population Simulations")

app_options = ["Global Population Evolution"]
selected_app = st.selectbox("Choose a Feature", app_options)

if selected_app == "Global Population Evolution":
    if st.button('Start Counting'):
        total_people_estimate, population_data = people_ever_lived()

        # Make the result human-readable and display it in billions
        st.success(f"An Estimated **{total_people_estimate:,.2f} billion** People Have Ever Lived on Earth.")
        
        # Plot the population evolution
        fig, ax = plt.subplots()
        ax.plot(population_data["years"], population_data["total_population"], label="Total People Ever Lived", color='blue')
        ax.set_xlabel("Year")
        ax.set_ylabel("Total People (Billions)")
        ax.set_title("Evolution of Total People Who Have Ever Lived")
        ax.grid(True)
        ax.legend()
        st.pyplot(fig)

elif selected_app == "Country Population Evolution":
    country = st.selectbox('Select a Country', list(countries_data.keys()))
    if st.button('Start Counting'):
        total_people_estimate = estimate_population_ever_lived(countries_data[country])
        st.success(f"Final Estimate of People Who Have Ever Lived in {country}: {total_people_estimate:.2f} billion")

elif selected_app == "Logistic Growth Projection":
    country = st.selectbox('Select a Country', list(historical_population_data.keys()))
    if st.button('Project Population'):
        population_projection(country)

elif selected_app == "Refined Population Projection":
    country = st.selectbox('Select a Country', list(refined_population_data.keys()))
    scenario = st.selectbox("Select a Future Growth Scenario", ["High Growth", "Moderate Growth", "Low Growth"])
    if st.button('Run Projection'):
        refined_population_projection(country, scenario)