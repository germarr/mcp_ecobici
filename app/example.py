"""
Example script showing how to use the BikeTrip class from the models module.
This script demonstrates how to create, query, and manipulate BikeTrip objects.
"""

import os
import sys
import pandas as pd
from sqlmodel import Session, create_engine, select
from app.models import BikeTrip

# Create SQLite database engine
DATABASE_URL = "sqlite:///bike_sharing.db"
engine = create_engine(DATABASE_URL, echo=True)

def create_sample_bike_trip():
    """Create a sample BikeTrip object and save it to the database."""
    # Create a sample bike trip
    sample_trip = BikeTrip(
        genero_usuario="M",
        edad_usuario=32,
        bici="ECOB-12345",
        ciclo_estacion_retiro="123",
        fecha_retiro="2025-06-19",
        ciclo_estacionarribo="456",
        fecha_arribo="2025-06-19",
        fecha_retiro_completa="2025-06-19 08:30:00",
        fecha_arribo_completa="2025-06-19 08:45:00",
        time_between_trips=15.0,
        day_of_the_week="Thursday",
        is_weekend=0,
        lat_start=19.4326,
        lon_start=-99.1332,
        lat_end=19.4275,
        lon_end=-99.1276,
        distance_meters=800.5,
        hora_retiro="08:30:00",
        hora_arribo="08:45:00"
    )
    
    # Save to the database
    with Session(engine) as session:
        session.add(sample_trip)
        session.commit()
        print(f"Created sample bike trip with ID: {sample_trip.id}")
        return sample_trip.id

def get_bike_trips(limit=10):
    """Query bike trips from the database."""
    with Session(engine) as session:
        trips = session.exec(select(BikeTrip).limit(limit)).all()
        for trip in trips:
            print(f"Trip ID: {trip.id}, From: {trip.ciclo_estacion_retiro}, To: {trip.ciclo_estacionarribo}")

def load_trips_from_parquet(file_path):
    """Load bike trips from a Parquet file and insert into the database."""
    if not os.path.exists(file_path):
        print(f"Error: File {file_path} not found")
        return
    
    print(f"Loading data from {file_path}...")
    try:
        # Read Parquet file using pandas
        df = pd.read_parquet(file_path)
        print(f"Loaded {len(df)} records from Parquet file")
        
        # Convert to BikeTrip objects and save to database
        with Session(engine) as session:
            # Limit to 100 records for demo purposes
            for _, row in df.head(100).iterrows():
                trip = BikeTrip(**row.to_dict())
                session.add(trip)
            session.commit()
        print("Data loaded successfully into database")
    except Exception as e:
        print(f"Error loading data: {e}")

if __name__ == "__main__":
    # Create the database tables if they don't exist
    from sqlmodel import SQLModel
    SQLModel.metadata.create_all(engine)
    
    # Create a sample trip
    sample_id = create_sample_bike_trip()
    
    # Query and display trips
    get_bike_trips()
    
    # Uncomment to load data from Parquet file
    # parquet_file = "notebooks/data/2025_01.parquet"
    # load_trips_from_parquet(parquet_file)