import geopandas as gpd

print("Loading shapefile...")
gdf = gpd.read_file("data/processed/king_county_displacement_risk.shp")

print(f"Tracts loaded: {len(gdf)}")
print(f"CRS: {gdf.crs}")

# Export as GeoJSON
output_path = "data/processed/king_county_displacement_risk.geojson"
gdf.to_file(output_path, driver="GeoJSON")

print(f"Saved to {output_path}")