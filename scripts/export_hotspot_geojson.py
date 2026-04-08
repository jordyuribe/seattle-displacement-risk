import geopandas as gpd

print("Loading hot spot analysis layer...")
gdf = gpd.read_file(r"C:\Users\jordy\Projects\seattle-displacement-risk\data\processed\Seattle-Displacement-Risk.gdb", layer="Hot_Spot_Analysis")

print(f"Tracts loaded: {len(gdf)}")
print(f"CRS: {gdf.crs}")

# Reproject to WGS84 for web mapping
gdf = gdf.to_crs(epsg=4326)

# Export as GeoJSON
output_path = "data/processed/hot_spot_analysis.geojson"
gdf.to_file(output_path, driver="GeoJSON")

print(f"Saved to {output_path}")