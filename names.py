import pandas as pd
import os
import argparse


def main(name, year, comparison="equal"):
    # Define the path to the directory where you extracted the files
    directory = "names"  # Update this path

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
    print(f"Total number of babies named {name} {comparison} {year}: {total_babies}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process baby names data.")
    parser.add_argument("--name", type=str, required=True, help="Name to search for")
    parser.add_argument("--year", type=int, required=True, help="Year for comparison")
    parser.add_argument(
        "--comparison",
        type=str,
        choices=["before", "equal", "after"],
        default="equal",
        help="Comparison operator for year (default: equal)",
    )

    args = parser.parse_args()
    main(args.name, args.year, args.comparison)
