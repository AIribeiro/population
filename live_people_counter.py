import time
import streamlit as st
from datetime import datetime
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

# Define historical population estimates and births between benchmarks based on updated projections
def people_ever_lived():
    periods = [
        {"start": -190000, "end": -50000, "population": 2, "birth_rate": 80, "births_between": 7856100000},  # 190,000 AC to 50,000 AC
        {"start": -50000, "end": -8000, "population": 2000000, "birth_rate": 80, "births_between": 1137789769},  # 50,000 AC to 8,000 AC
        {"start": -8000, "end": 1, "population": 5000000, "birth_rate": 80, "births_between": 46025332354},  # 8,000 AC to 1 DC
        {"start": 1, "end": 1200, "population": 300000000, "birth_rate": 80, "births_between": 26591343000},  # 1 DC to 1200 DC
        {"start": 1200, "end": 1650, "population": 450000000, "birth_rate": 60, "births_between": 12782002453},  # 1200 DC to 1650 DC
        {"start": 1650, "end": 1750, "population": 500000000, "birth_rate": 60, "births_between": 3171931513},  # 1650 DC to 1750 DC
        {"start": 1750, "end": 1850, "population": 795000000, "birth_rate": 50, "births_between": 4046240009},  # 1750 DC to 1850 DC
        {"start": 1850, "end": 1900, "population": 1265000000, "birth_rate": 40, "births_between": 2900237856},  # 1850 DC to 1900 DC
        {"start": 1900, "end": 1950, "population": 1656000000, "birth_rate": 31, "births_between": 3390198215},  # 1900 DC to 1950 DC
        {"start": 1950, "end": 2000, "population": 2499000000, "birth_rate": 22, "births_between": 6064994884},  # 1950 DC to 2000 DC
        {"start": 2000, "end": 2022, "population": 6149000000, "birth_rate": 17, "births_between": 1690275115},  # 2000 DC to 2022 DC
        {"start": 2023, "end": 2024, "population": 8050000000, "birth_rate": 17, "births_between": 1090000000},  # 2023 DC to 2024 DC
    ]

    total_births = 2  # Start with the smallest initial value to reflect early humanity
    population_data = {"years": [], "total_population": []}  # To store years and population for plotting
    plot_data = {"years": [], "total_population": []}  # Plot specific years for visualization

    # Streamlit display for the live counter and plot
    counter_placeholder = st.empty()
    plot_placeholder = st.empty()

    # Hardcoded adjustment to reach the exact number for 2024
    adjustment_factor = 117020448575 - 115930445170  # Adjust to reach 117 billion in 2024
    adjustment_per_year = adjustment_factor / 2  # Spread adjustment across 2023 and 2024

    # Calculate the total number of years and determine the sleep time per year
    total_years = sum(period["end"] - period["start"] + 1 for period in periods)
    total_duration = 10  # 10 seconds for the entire simulation
    sleep_time = total_duration / total_years  # Time to sleep for each year to fit within 10 seconds

    # Initialize a figure for live plotting
    fig, ax = plt.subplots()
    ax.set_xlabel("Year")
    ax.set_ylabel("Total Births")
    ax.set_title("Evolution of Total Births")
    ax.grid(True)

    # Loop through each period and accumulate the total number of births based on the data provided
    for period in periods:
        births_between = period["births_between"]

        # Simulate the population count for each year in the period
        for year in range(period["start"], period["end"] + 1):
            # Calculate the average yearly births during the period
            yearly_births = births_between / (period["end"] - period["start"] + 1)

            # Apply the adjustment factor in the final two years (2023-2024)
            if year == 2023 or year == 2024:
                yearly_births += adjustment_per_year

            total_births += yearly_births  # Add yearly births incrementally
            population_data["years"].append(year)
            population_data["total_population"].append(total_births)

            # Display years as AC for years before 0 and DC for years after 0
            display_year = f"{abs(year)} AC" if year < 0 else f"{year} DC"
            
            # Update the live counter for all years
            counter_placeholder.markdown(f"### Year: {display_year}, Total Births So Far: **{total_births:,.0f}.**".replace(',', '.'))

            # Plot every 10,000 years until year 0, then every 10 years after year 1 DC
            if (year % 10000 == 0 and year <= 0) or (year % 10 == 0 and year > 0):
                plot_data["years"].append(year)
                plot_data["total_population"].append(total_births)

                # Update the plot live
                ax.clear()
                ax.plot(plot_data["years"], plot_data["total_population"], label="Total Births", color='blue')
                ax.set_xlabel("Year")
                ax.set_ylabel("Total Births")
                ax.set_title("Evolution of Total Births")

                # Adapt the scale to better visualize years after year 0 (DC)
                if year >= 0:
                    ax.set_xlim([0, 2024])  # Focus on the years from year 0 to 2024
                else:
                    ax.set_xlim([-190000, 0])  # For years before 0 AC

                ax.grid(True)

                # Improve readability of numbers in the plot
                ax.yaxis.set_major_formatter(ticker.FuncFormatter(lambda x, pos: f'{x:,.0f}'.replace(',', '.')))
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
    st.success(f"We estimate that {total_people_estimate:,.0f} people have ever been born on this planet.".replace(',', '.'))

# Footer section
st.markdown("***")
st.markdown("Developed by [Jair Ribeiro](https://www.linkedin.com/in/jairribeiro/). For more details, read the full article on [How Many Humans Have Ever Lived on Our Planet?](https://jairribeiro.medium.com/how-many-humans-have-ever-lived-on-our-planet-306f770fc2c4)")
