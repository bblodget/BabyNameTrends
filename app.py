import streamlit as st
import pandas as pd
import os
import altair as alt


def load_data(directory, name, year, comparison):
    # Initialize an empty DataFrame to hold all the data
    all_data = pd.DataFrame()

    # Loop through each file in the directory
    for filename in os.listdir(directory):
        if filename.startswith("yob") and filename.endswith(".txt"):
            file_year = int(filename[3:7])

            # Apply the comparison filter
            if (
                (comparison == "before" and file_year <= year)
                or (comparison == "equal" and file_year == year)
                or (comparison == "after" and file_year >= year)
            ):
                # Read the data from the file
                yearly_data = pd.read_csv(
                    os.path.join(directory, filename), names=["Name", "Gender", "Count"]
                )
                yearly_data["Year"] = file_year
                # Append to the main DataFrame
                all_data = pd.concat([all_data, yearly_data])

    # Ensure the 'Year' column is numeric and remove commas
    all_data["Year"] = all_data["Year"].apply(lambda x: int(str(x).replace(",", "")))

    # Filter for the specified name
    filtered_data = all_data[all_data["Name"].str.lower() == name.lower()]

    # Group by year and sum counts to avoid multiple data points for the same year
    grouped_data = filtered_data.groupby("Year").sum().reset_index()

    # Calculate the total number of babies with the specified name based on the comparison
    total_babies = grouped_data["Count"].sum()
    return grouped_data, total_babies, all_data


def get_top_names(data, year):
    # Ensure the 'Year' column is numeric
    data["Year"] = pd.to_numeric(data["Year"], errors="coerce")

    # Filter data for the selected year
    year_data = data[data["Year"] == year]

    # Get top 10 boy names and top 10 girl names
    top_boys = year_data[year_data["Gender"] == "M"].nlargest(10, "Count")
    top_girls = year_data[year_data["Gender"] == "F"].nlargest(10, "Count")
    return top_boys, top_girls


def main():
    st.title("US Baby Names Analysis")

    # User inputs
    name = st.text_input("Enter the name:", "Brandon")
    year = st.number_input(
        "Enter the year:", min_value=1880, max_value=2023, value=1970
    )
    comparison = st.selectbox(
        "Select comparison:", ["equal", "before", "after"], index=1
    )

    # Path to the local "names" directory
    directory = os.path.join(os.path.dirname(__file__), "names")

    if os.path.exists(directory):
        # Load and process data
        grouped_data, total_babies, all_data = load_data(
            directory, name, year, comparison
        )

        st.write(
            f"Total number of babies named {name} {comparison} {year}: {total_babies}"
        )

        # Visualization using Altair
        if not grouped_data.empty:
            chart = (
                alt.Chart(grouped_data)
                .mark_line(point=True)
                .encode(
                    x=alt.X(
                        "Year", axis=alt.Axis(format="d")
                    ),  # Remove commas from years
                    y="Count",
                    tooltip=["Year", "Count"],
                )
                .interactive()
            )

            st.altair_chart(chart, use_container_width=True)

        # Top names for the selected year
        top_boys, top_girls = get_top_names(all_data, year)

        # st.write(f"Top 10 boy names in {year}:")
        if not top_boys.empty:
            boys_chart = (
                alt.Chart(top_boys)
                .mark_bar()
                .encode(
                    x="Count:Q", y=alt.Y("Name:N", sort="-x"), tooltip=["Name", "Count"]
                )
                .properties(title=f"Top 10 Boy Names in {year}")
            )
            st.altair_chart(boys_chart, use_container_width=True)

        # st.write(f"Top 10 girl names in {year}:")
        if not top_girls.empty:
            girls_chart = (
                alt.Chart(top_girls)
                .mark_bar()
                .encode(
                    x="Count:Q", y=alt.Y("Name:N", sort="-x"), tooltip=["Name", "Count"]
                )
                .properties(title=f"Top 10 Girl Names in {year}")
            )
            st.altair_chart(girls_chart, use_container_width=True)
    else:
        st.error(f'Directory "{directory}" does not exist.')


if __name__ == "__main__":
    main()
