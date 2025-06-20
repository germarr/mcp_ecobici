"""
This script demonstrates how to run the Ecobici application.
It imports from app.models, creates sample data, and starts the FastAPI server.
"""

import os
import sys
from sqlmodel import SQLModel, create_engine, Session, select
import uvicorn

# Add project root to path if needed
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import our models
from app.models import BikeTrip
from app.main import app, BikeStation, engine

def setup_database():
    """Create database tables and add sample data if needed."""
    print("Setting up database...")
    
    # Create tables
    SQLModel.metadata.create_all(engine)
    
    # Check if we have any bike trips
    with Session(engine) as session:
        trips = session.exec(select(BikeTrip)).first()
        if not trips:
            print("Adding sample bike trip data...")
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
            session.add(sample_trip)
            session.commit()
            print(f"Created sample bike trip with ID: {sample_trip.id}")

if __name__ == "__main__":
    # Setup database
    setup_database()
    
    # Run the FastAPI application
    print("Starting Ecobici API server...")
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
