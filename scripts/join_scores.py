import geopandas as gpd
import pandas as pd

print("Loading Washington State tract shapefile...")
gdf = gpd.read_file("data/raw/wa_tracts/tl_2023_53_tract.shp")
print(f"Total WA tracts: {len(gdf)}")

# Filter to King County only (FIPS county code 033)
king = gdf[gdf["COUNTYFP"] == "033"].copy()
print(f"King County tracts: {len(king)}")

# Load your risk scores
print("\nLoading displacement risk scores...")
scores = pd.read_csv("data/processed/displacement_risk_scores.csv")
print(f"Scored tracts: {len(scores)}")

# The shapefile uses TRACTCE (e.g. "000101")
# Your CSV has a tract column in the same format
# We join on that field
king["TRACTCE"] = king["TRACTCE"].astype(str)
scores["tract"] = scores["tract"].astype(str).str.zfill(6)

merged = king.merge(scores, left_on="TRACTCE", right_on="tract", how="left")
print(f"Merged tracts: {len(merged)}")
print(f"Tracts with risk scores: {merged['displacement_risk_score'].notna().sum()}")

# Check coordinate reference system
print(f"\nCoordinate system: {merged.crs}")

# Reproject to WGS84 (EPSG:4326) — standard for web maps and ArcGIS Online
merged = merged.to_crs(epsg=4326)
print("Reprojected to WGS84 (EPSG:4326)")

# Preview
print("\nSample output:")
print(merged[["TRACTCE", "displacement_risk_score", "pct_renters", "pct_cost_burdened"]].head())

# Save as shapefile for ArcGIS Pro
output_path = "data/processed/king_county_displacement_risk.shp"
merged.to_file(output_path)
print(f"\nSaved to {output_path}")