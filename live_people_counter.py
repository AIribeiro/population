import time
import streamlit as st
from datetime import datetime
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

# Define historical population estimates and births between benchmarks based on the article data and updated projections
def people_ever_lived():
    periods = [
        {"start": -190000, "end": -50000, "population": 2, "birth_rate": 80, "births_between": 7856100000},  # 190,000 B.C.E. to 50,000 B.C.E.
        {"start": -50000, "end": -8000, "population": 2000000, "birth_rate": 80, "births_between": 1137789769},  # 50,000 B.C.E. to 8000 B.C.E.
        {"start": -8000, "end": 1, "population": 5000000, "birth_rate": 80, "births_between": 46025332354},  # 8000 B.C.E. to 1 C.E.
        {"start": 1, "end": 1200, "population": 300000000, "birth_rate": 80, "births_between": 26591343000},  # 1 C.E. to 1200 C.E.
        {"start": 1200, "end": 1650, "population": 450000000, "birth_rate": 60, "births_between": 12782002453},  # 1200 C.E. to 1650 C.E.
        {"start": 1650, "end": 1750, "population": 500000000, "birth_rate": 60, "births_between": 3171931513},  # 1650 C.E. to 1750 C.E.
        {"start": 1750, "end": 1850, "population": 795000000, "birth_rate": 50, "births_between": 4046240009},  # 1750 C.E. to 1850 C.E.
        {"start": 1850, "end": 1900, "population": 1265000000, "birth_rate": 40, "births_between": 2900237856},  # 1850 C.E. to 1900 C.E.
        {"start": 1900, "end": 1950, "population": 1656000000, "birth_rate": 31, "births_between": 3390198215},  # 1900 C.E. to 1950 C.E.
        {"start": 1950, "end": 2000, "population": 2499000000, "birth_rate": 22, "births_between": 6064994884},  # 1950 C.E. to 2000 C.E.
        {"start": 2000, "end": 2022, "population": 6149000000, "birth_rate": 17, "births_between": 1690275115},  # 2000 C.E. to 2022 C.E.
        {"start": 2023, "end": 2024, "population": 8050000000, "birth_rate": 17, "births_between": 135000000},  # 2023 to 2024 C.E.
        {"start": 2024, "end": 2035, "population": 8100000000, "birth_rate": 16, "births_between": 900000000},  # 2024 to 2035 C.E.
        {"start": 2035, "end": 2050, "population": 9000000000, "birth_rate": 14, "births_between": 966000000},  # 2035 to 2050 C.E.
    ]

    total_births = 0
    population_data = {"years": [], "total_population": []}  # To store years and population for plotting
    plot_data = {"years": [], "total_population": []}  # Plot only from year 1 C.E. and every 10 years

    # Streamlit display for the live counter and plot
    counter_placeholder = st.empty()
    plot_placeholder = st.empty()

    # Calculate the total number of years and determine the sleep time per year
    total_years = sum(period["end"] - period["start"] + 1 for period in periods)
    total_duration = 10  # 10 seconds for the entire simulation
    sleep_time = total_duration / total_years  # Time to sleep for each year to fit within 10 seconds

    # Initialize a figure for live plotting
    fig, ax = plt.subplots()
    ax.set_xlabel("Year")
    ax.set_ylabel("Total Births")
    ax.set_title("Evolution of Total Births from Year 1 C.E.")
    ax.grid(True)

    # Variable to control how frequently to update the plot (every 10 years)
    update_interval = 10  # Update the plot every 10 years

    # Loop through each period and accumulate the total number of births based on the data provided
    for period in periods:
        births_between = period["births_between"]
        total_births += births_between  # Directly adding births between periods as specified

        # Simulate the population count for each year in the period
        for year in range(period["start"], period["end"] + 1):
            population_data["years"].append(year)
            population_data["total_population"].append(total_births)

            # Update the live counter for all years
            counter_placeholder.markdown(f"### Year: {year}, Total Births So Far: **{total_births:,.0f}.**")

            # Only start plotting from year 1 C.E. and update every 10 years
            if year >= 1 and year % update_interval == 0:
                plot_data["years"].append(year)
                plot_data["total_population"].append(total_births)

                # Update the plot live every 10 years
                ax.clear()
                ax.plot(plot_data["years"], plot_data["total_population"], label="Total Births", color='blue')
                ax.set_xlabel("Year")
                ax.set_ylabel("Total Births")
                ax.set_title("Evolution of Total Births from Year 1 C.E.")
                ax.grid(True)

                # Improve readability of numbers in the plot
                ax.yaxis.set_major_formatter(ticker.FuncFormatter(lambda x, pos: f'{x:,.0f}'))
                ax.xaxis.set_major_locator(ticker.MaxNLocator(10))  # Set a maximum of 10 ticks on the x-axis
                plt.xticks(rotation=45, ha="right")  # Rotate year labels by 45 degrees for better readability
                ax.legend()

                # Display the updated plot
                plot_placeholder.pyplot(fig)

            time.sleep(sleep_time)  # Ensure the sleep time fits within the 10 seconds

    return total_births, population_data

# Streamlit UI
st.title("Live Counter: People Who Have Ever Lived")
st.write("This app simulates a live counter of the estimated number of people who have ever been born since the emergence of Homo sapiens.")

# Start the simulation
if st.button('Start Counting'):
    total_people_estimate, population_data = people_ever_lived()
    st.success(f"We estimate that {total_people_estimate:,.0f} people have ever been born on this planet.")