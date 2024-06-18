# BabyNameTrends

BabyNameTrends is a Streamlit app that allows users to explore historical trends in baby names in the United States. You can view the popularity of specific names over time and discover the top baby names for any given year.

## Features

- **Name Trends:** View the popularity of a specific name over the years.
- **Top Names:** Discover the top 10 boy and girl names for a selected year.
- **Interactive Charts:** Hover over and click on the charts to see detailed data points.

## Dataset

The dataset used for this app is provided by the U.S. Social Security Administration (SSA) and can be found at the following URL:

[https://www.ssa.gov/oact/babynames/limits.html](https://www.ssa.gov/oact/babynames/limits.html)

## Installation

To run this app locally, follow these steps:

1. **Clone the repository:**
   ```
   git clone https://github.com/yourusername/baby-name-trends.git
   cd baby-name-trends
   ```

2. **Create and activate a virtual environment:**
   ```
   python3 -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install the required packages:**
   ```
   pip install -r requirements.txt
   ```

4. **Run the app:**
   ```
   streamlit run app.py
   ```

## Usage

1. **Enter a name** to see its popularity over the years.
2. **Select a year** to view the top 10 boy and girl names for that year.
3. **Choose a comparison** (equal, before, after) to filter the data accordingly.
