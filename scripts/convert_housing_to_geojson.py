#!/usr/bin/env python3
"""
Convert housing.json to GeoJSON format for Koop server.

This script reads the housing data from ../lotspy/data/housing.json
and converts it to GeoJSON format with Point geometries based on
the Latitude/Longitude coordinates.
"""

import json
import os
from typing import Dict, List, Any


def load_housing_data(input_file: str) -> List[Dict[str, Any]]:
    """Load housing data from JSON file."""
    with open(input_file, 'r') as f:
        return json.load(f)


def create_geojson_feature(housing_record: Dict[str, Any]) -> Dict[str, Any]:
    """Convert a single housing record to a GeoJSON feature."""
    # Create the geometry from lat/lon (note: lowercase field names)
    # Handle both string and numeric coordinate types
    lon = housing_record["longitude"]
    lat = housing_record["latitude"]
    if isinstance(lon, str):
        lon = float(lon)
    if isinstance(lat, str):
        lat = float(lat)
    
    geometry = {
        "type": "Point",
        "coordinates": [lon, lat]
    }
    
    # Create properties by copying all fields except lat/lon
    properties = {k: v for k, v in housing_record.items() 
                  if k not in ["latitude", "longitude"]}
    
    return {
        "type": "Feature",
        "geometry": geometry,
        "properties": properties
    }


def convert_to_geojson(housing_data: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Convert housing data to GeoJSON FeatureCollection."""
    features = []
    
    for record in housing_data:
        # Skip records without valid coordinates
        lat = record.get("latitude", "")
        lon = record.get("longitude", "")
        
        if (not lat or not lon or 
            lat in ["0", "0.0", 0, 0.0] or 
            lon in ["0", "0.0", 0, 0.0] or
            lat == "" or lon == ""):
            continue
            
        try:
            # Test if coordinates can be converted to float
            if isinstance(lat, str):
                float(lat)
            if isinstance(lon, str):
                float(lon)
            # Also check for numeric zeros
            if lat == 0 or lon == 0:
                continue
        except (ValueError, TypeError):
            continue
            
        feature = create_geojson_feature(record)
        features.append(feature)
    
    return {
        "type": "FeatureCollection",
        "features": features
    }


def main():
    """Main conversion function."""
    # Define file paths
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)
    input_file = os.path.join(project_root, "..", "lotspy", "data", "housing.json")
    output_file = os.path.join(project_root, "provider-data", "housing.geojson")
    
    # Check if input file exists
    if not os.path.exists(input_file):
        print(f"Error: Input file not found: {input_file}")
        return 1
    
    try:
        # Load and convert data
        print(f"Loading housing data from: {input_file}")
        housing_data = load_housing_data(input_file)
        print(f"Loaded {len(housing_data)} housing records")
        
        # Convert to GeoJSON
        geojson_data = convert_to_geojson(housing_data)
        print(f"Converted to {len(geojson_data['features'])} GeoJSON features")
        
        # Write output file
        with open(output_file, 'w') as f:
            json.dump(geojson_data, f, indent=2)
        
        print(f"GeoJSON file created: {output_file}")
        print("Conversion completed successfully!")
        
        return 0
        
    except Exception as e:
        print(f"Error during conversion: {e}")
        return 1


if __name__ == "__main__":
    exit(main())