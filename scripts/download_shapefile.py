import requests
import zipfile
import os

print("Downloading King County census tract shapefile...")

# Census TIGER/Line shapefile for Washington State census tracts (2023)
# We download the whole state and will clip to King County in the next step
url = "https://www2.census.gov/geo/tiger/TIGER2023/TRACT/tl_2023_53_tract.zip"

# Download the file
response = requests.get(url, stream=True)

if response.status_code != 200:
    print(f"Error: {response.status_code}")
else:
    # Save the zip file
    zip_path = "data/raw/wa_tracts.zip"
    with open(zip_path, "wb") as f:
        for chunk in response.iter_content(chunk_size=8192):
            f.write(chunk)
    print("Download complete. Extracting...")

    # Extract the zip
    extract_path = "data/raw/wa_tracts"
    os.makedirs(extract_path, exist_ok=True)

    with zipfile.ZipFile(zip_path, "r") as z:
        z.extractall(extract_path)

    print("Extracted files:")
    for file in os.listdir(extract_path):
        print(f"  {file}")

    print("\nShapefile ready at data/raw/wa_tracts/")