import pandas as pd
import os

# Define the path to the directory where you extracted the files
directory = "names"  # Update this path

# Initialize an empty DataFrame to hold all the data
all_data = pd.DataFrame()

# Loop through each file in the directory
for filename in os.listdir(directory):
    if filename.startswith("yob") and filename.endswith(".txt"):
        year = int(filename[3:7])
        if year < 1974:
            # Read the data from the file
            yearly_data = pd.read_csv(
                os.path.join(directory, filename), names=["Name", "Gender", "Count"]
            )
            yearly_data["Year"] = year
            # Append to the main DataFrame
            all_data = pd.concat([all_data, yearly_data])

# Filter for the name "Brandon"
brandon_data_pre_1970 = all_data[all_data["Name"] == "Evan"]

# Calculate the total number of babies named Brandon before 1970
total_babies_named_brandon_pre_1970 = brandon_data_pre_1970["Count"].sum()
print(
    f"Total number of babies named Brandon before 1970: {total_babies_named_brandon_pre_1970}"
)
