import requests
import pandas as pd

print("Script is running")

# Your Census API key
from dotenv import load_dotenv
import os

load_dotenv()
API_KEY = os.getenv("API_KEY")

# We're pulling ACS 5-year 2023 data
# at the census tract level for King County, WA (FIPS: state=53, county=033)
BASE_URL = "https://api.census.gov/data/2023/acs/acs5"

# The variables we want to pull
# Each code maps to a specific ACS table
VARIABLES = {
    "B25003_001E": "total_housing_units",       # Total occupied housing units
    "B25003_002E": "owner_occupied",            # Owner occupied
    "B25003_003E": "renter_occupied",           # Renter occupied
    "B19013_001E": "median_household_income",   # Median household income
    "B25070_007E": "rent_burden_30_34",         # Renters paying 30-34% on rent
    "B25070_008E": "rent_burden_35_39",         # Renters paying 35-39% on rent
    "B25070_009E": "rent_burden_40_49",         # Renters paying 40-49% on rent
    "B25070_010E": "rent_burden_50_plus",       # Renters paying 50%+ on rent
    "B25070_001E": "rent_burden_total",         # Total renters (denominator)
    "B15003_001E": "education_total",           # Total population 25+ (denominator)
    "B15003_002E": "no_schooling",              # No schooling completed
    "B15003_003E": "nursery_school",            # Nursery school
    "B03002_001E": "total_population",          # Total population
    "B03002_003E": "white_non_hispanic",        # White non-Hispanic
}

def fetch_census_data():
    # Build the variable string for the API request
    var_string = ",".join(VARIABLES.keys())

    # Build the full API URL
    params = {
        "get": f"NAME,{var_string}",
        "for": "tract:*",
        "in": "state:53 county:033",  # Washington State, King County
        "key": API_KEY
    }

    print("Fetching Census data...")
    response = requests.get(BASE_URL, params=params)

    # Check if the request worked
    if response.status_code != 200:
        print(f"Error: {response.status_code}")
        print(response.text)
        return None

    # Parse the response into a DataFrame
    data = response.json()
    headers = data[0]
    rows = data[1:]
    df = pd.DataFrame(rows, columns=headers)

    # Rename columns to human-readable names
    df = df.rename(columns=VARIABLES)

    # Convert numeric columns from strings to numbers
    numeric_cols = list(VARIABLES.values())
    df[numeric_cols] = df[numeric_cols].apply(pd.to_numeric, errors="coerce")

    print(f"Success! Pulled {len(df)} census tracts.")
    print(df.head())

    df.to_csv("data/raw/king_county_acs.csv", index=False)
    print("Saved to data/raw/king_county_acs.csv")

    return df

if __name__ == "__main__":
    df = fetch_census_data()