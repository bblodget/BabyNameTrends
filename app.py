import streamlit as st
import pandas as pd
import os
import matplotlib.pyplot as plt
import seaborn as sns


def load_data(directory, name, year, comparison):
    # Initialize an empty DataFrame to hold all the data
    all_data = pd.DataFrame()

    # Loop through each file in the directory
    for filename in os.listdir(directory):
        if filename.startswith("yob") and filename.endswith(".txt"):
            file_year = int(filename[3:7])

            # Apply the comparison filter
            if (
                (comparison == "before" and file_year < year)
                or (comparison == "equal" and file_year == year)
                or (comparison == "after" and file_year > year)
            ):
                # Read the data from the file
                yearly_data = pd.read_csv(
                    os.path.join(directory, filename), names=["Name", "Gender", "Count"]
                )
                yearly_data["Year"] = file_year
                # Append to the main DataFrame
                all_data = pd.concat([all_data, yearly_data])

    # Filter for the specified name
    filtered_data = all_data[all_data["Name"].str.lower() == name.lower()]

    # Calculate the total number of babies with the specified name based on the comparison
    total_babies = filtered_data["Count"].sum()
    return filtered_data, total_babies


def main():
    st.title("US Baby Names Analysis")

    # User inputs
    name = st.text_input("Enter the name:", "Brandon")
    year = st.number_input(
        "Enter the year:", min_value=1880, max_value=2023, value=1970
    )
    comparison = st.selectbox("Select comparison:", ["equal", "before", "after"])

    # Path to the local "names" directory
    directory = os.path.join(os.path.dirname(__file__), "names")

    if os.path.exists(directory):
        # Load and process data
        filtered_data, total_babies = load_data(directory, name, year, comparison)

        st.write(
            f"Total number of babies named {name} {comparison} {year}: {total_babies}"
        )

        # Visualization
        if not filtered_data.empty:
            plt.figure(figsize=(10, 6))
            sns.lineplot(data=filtered_data, x="Year", y="Count", marker="o")
            plt.title(
                f"Number of Babies Named {name.capitalize()} {comparison.capitalize()} {year}"
            )
            plt.xlabel("Year")
            plt.ylabel("Count")
            plt.grid(True)
            st.pyplot(plt)
    else:
        st.error(f'Directory "{directory}" does not exist.')


if __name__ == "__main__":
    main()
