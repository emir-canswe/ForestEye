import os
import sys
from pathlib import Path
from shapely.geometry import Polygon
from sqlalchemy.orm import Session
from sqlalchemy import text

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from app.core.database import SessionLocal, engine
from app.models.db.models import GridCell
import json

# Turkey bounding box approximate
LAT_MIN = 35.8
LAT_MAX = 42.1
LON_MIN = 25.6
LON_MAX = 44.8
GRID_SIZE = 0.1

def create_grid_cells():
    print("Generating 0.1 degree grid cells for Turkey...")
    db: Session = SessionLocal()
    
    # Check if grid cells already exist
    count = db.query(GridCell).count()
    if count > 0:
        print(f"Grid cells already exist ({count} cells). Skipping generation.")
        db.close()
        return

    # To use PostGIS, we might want to make sure the extension is enabled
    try:
        db.execute(text("CREATE EXTENSION IF NOT EXISTS postgis;"))
        db.commit()
    except Exception as e:
        print(f"Warning: Could not create postgis extension automatically: {e}")
        db.rollback()

    cells = []
    lat = LAT_MIN
    while lat < LAT_MAX:
        lon = LON_MIN
        while lon < LON_MAX:
            # Create a polygon for the grid cell
            poly = Polygon([
                (lon, lat),
                (lon + GRID_SIZE, lat),
                (lon + GRID_SIZE, lat + GRID_SIZE),
                (lon, lat + GRID_SIZE),
                (lon, lat) # close polygon
            ])
            
            # WKT representation
            wkt = poly.wkt
            
            lat_center = lat + (GRID_SIZE / 2)
            lon_center = lon + (GRID_SIZE / 2)
            
            cell = GridCell(
                geom=f"SRID=4326;{wkt}",
                lat_center=lat_center,
                lon_center=lon_center,
                # In a real scenario, we'd do a spatial join to get the actual province (il_adi) 
                # or use a reverse geocoding API.
            )
            cells.append(cell)
            
            lon += GRID_SIZE
        lat += GRID_SIZE
        
    print(f"Generated {len(cells)} cells. Inserting into database...")
    
    # Bulk insert
    try:
        db.bulk_save_objects(cells)
        db.commit()
        print("Successfully inserted grid cells.")
    except Exception as e:
        db.rollback()
        print(f"Error inserting grid cells: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    create_grid_cells()
