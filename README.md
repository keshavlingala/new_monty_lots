# Koop GeoJSON Server

A Koop server for hosting GeoJSON data files with a Leaflet frontend that dynamically discovers and displays all available layers.

## Features

- **Dynamic Service Discovery**: Automatically scans and catalogs all GeoJSON files in the `provider-data` directory
- **Koop Integration**: Serves GeoJSON data through Koop's FeatureServer API
- **Interactive Map**: Leaflet-based frontend that loads and displays all available layers
- **Service Catalog**: RESTful endpoint at `/catalog` that lists all available services

## Quick Start

1. Install dependencies:
   ```bash
   npm install
   ```

2. Start the server:
   ```bash
   npm start
   ```

3. Open your browser to http://localhost:8080

## API Endpoints

- **`/`** - Interactive map interface
- **`/catalog`** - Service catalog listing all available GeoJSON layers
- **`/file-geojson/rest/services/{layer}/FeatureServer`** - Koop FeatureServer endpoint for each layer
- **`/file-geojson/rest/services/{layer}/FeatureServer/0/query`** - Query endpoint for GeoJSON data

## Adding Data

Simply add `.geojson` files to the `provider-data/` directory. The server will automatically discover and serve them through the Koop API.

## Development

```bash
npm run dev  # Start with nodemon for auto-restart
```

## Data Files

The `provider-data/` directory contains sample GeoJSON files:
- Points, polygons, lines, and complex geometries
- Various coordinate systems and metadata examples