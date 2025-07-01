#!/usr/bin/env python3
"""
Convert registry.json to GeoJSON format for Koop server.
This script is adapted from convert_housing_to_geojson.py
"""

import json
import os
from typing import Dict, List, Any


def load_registry_data(input_file: str) -> List[Dict[str, Any]]:
    """Load registry data from JSON file."""
    with open(input_file, 'r') as f:
        return json.load(f)


def create_geojson_feature(registry_record: Dict[str, Any]) -> Dict[str, Any]:
    """Convert a single registry record to a GeoJSON feature."""
    # Handle both string and numeric coordinate types
    lon = registry_record["longitude"]
    lat = registry_record["latitude"]
    if isinstance(lon, str):
        lon = float(lon)
    if isinstance(lat, str):
        lat = float(lat)
    
    geometry = {
        "type": "Point",
        "coordinates": [lon, lat]
    }
    
    # Create properties by copying all fields except lat/lon
    properties = {k: v for k, v in registry_record.items() 
                  if k not in ["latitude", "longitude"]}
    
    return {
        "type": "Feature",
        "geometry": geometry,
        "properties": properties
    }


def convert_to_geojson(registry_data: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Convert registry data to GeoJSON FeatureCollection."""
    features = []
    
    for record in registry_data:
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
    input_file = os.path.join(project_root, "..", "lotspy", "data", "registry.json")
    output_file = os.path.join(project_root, "provider-data", "registry.geojson")
    
    # Check if input file exists
    if not os.path.exists(input_file):
        print(f"Error: Input file not found: {input_file}")
        return 1
    
    try:
        # Load and convert data
        print(f"Loading registry data from: {input_file}")
        registry_data = load_registry_data(input_file)
        print(f"Loaded {len(registry_data)} registry records")
        
        # Convert to GeoJSON
        geojson_data = convert_to_geojson(registry_data)
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