"""
Simple FastAPI application that interacts with an SQLite database.
This app demonstrates basic CRUD operations using dummy bike-sharing data.
Includes a landing page using Jinja templates.
"""

from fastapi import FastAPI, HTTPException, Depends, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlmodel import Field, Session, SQLModel, create_engine, select
from typing import List, Optional
import datetime
import os

# Define database model
class BikeStation(SQLModel, table=True):
    """Represents a bike station in the bike-sharing system."""
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    location: str
    capacity: int
    available_bikes: int
    last_updated: datetime.datetime = Field(default_factory=datetime.datetime.now)

# Create SQLite database engine
# Note: In a production environment, the database URL should be in a config file
DATABASE_URL = "sqlite:///bike_sharing.db"
engine = create_engine(DATABASE_URL, echo=True)

# Initialize FastAPI app
app = FastAPI(
    title="Ecobici API",
    description="API for a bike-sharing system using SQLite database",
    version="0.1.0"
)

# Set up templates and static files
templates_dir = os.path.join(os.path.dirname(__file__), "templates")
templates = Jinja2Templates(directory=templates_dir)
app.mount("/static", StaticFiles(directory=os.path.join(os.path.dirname(__file__), "static")), name="static")

# Dependency to get database session
def get_session():
    """Database session dependency."""
    with Session(engine) as session:
        yield session

# Create tables on startup
@app.on_event("startup")
def on_startup():
    """Create database tables and add dummy data if needed."""
    SQLModel.metadata.create_all(engine)
    
    # Add dummy data if database is empty
    with Session(engine) as session:
        stations = session.exec(select(BikeStation)).first()
        if not stations:
            dummy_stations = [
                BikeStation(
                    name="Central Park Station",
                    location="40.7812, -73.9665",
                    capacity=30,
                    available_bikes=15
                ),
                BikeStation(
                    name="Union Square",
                    location="40.7359, -73.9911",
                    capacity=25,
                    available_bikes=10
                ),
                BikeStation(
                    name="Brooklyn Heights",
                    location="40.6958, -73.9936",
                    capacity=20,
                    available_bikes=5
                ),
                BikeStation(
                    name="Times Square",
                    location="40.7580, -73.9855",
                    capacity=40,
                    available_bikes=20
                ),
                BikeStation(
                    name="Battery Park",
                    location="40.7033, -74.0170",
                    capacity=35,
                    available_bikes=17
                )
            ]
            for station in dummy_stations:
                session.add(station)
            session.commit()

# API Endpoints

@app.get("/")
async def root(request: Request):
    """Root endpoint that serves the landing page."""
    return templates.TemplateResponse("index.html", {"request": request, "title": "Ecobici Bike-Sharing"})

@app.get("/stations/", response_model=List[BikeStation])
async def get_all_stations(session: Session = Depends(get_session)):
    """Get all bike stations."""
    stations = session.exec(select(BikeStation)).all()
    return stations

@app.get("/stations/{station_id}", response_model=BikeStation)
async def get_station(station_id: int, session: Session = Depends(get_session)):
    """Get a specific bike station by ID."""
    station = session.get(BikeStation, station_id)
    if not station:
        raise HTTPException(status_code=404, detail="Station not found")
    return station

@app.post("/stations/", response_model=BikeStation)
async def create_station(station: BikeStation, session: Session = Depends(get_session)):
    """Create a new bike station."""
    session.add(station)
    session.commit()
    session.refresh(station)
    return station

@app.put("/stations/{station_id}", response_model=BikeStation)
async def update_station(station_id: int, updated_station: BikeStation, session: Session = Depends(get_session)):
    """Update an existing bike station."""
    db_station = session.get(BikeStation, station_id)
    if not db_station:
        raise HTTPException(status_code=404, detail="Station not found")
    
    # Update station attributes
    station_data = updated_station.dict(exclude_unset=True)
    for key, value in station_data.items():
        setattr(db_station, key, value)
    
    session.add(db_station)
    session.commit()
    session.refresh(db_station)
    return db_station

@app.delete("/stations/{station_id}")
async def delete_station(station_id: int, session: Session = Depends(get_session)):
    """Delete a bike station."""
    station = session.get(BikeStation, station_id)
    if not station:
        raise HTTPException(status_code=404, detail="Station not found")
    
    session.delete(station)
    session.commit()
    return {"message": f"Station {station_id} deleted successfully"}

@app.get("/stations/available")
async def get_available_bikes(min_bikes: int = 1, session: Session = Depends(get_session)):
    """Get stations with at least the specified number of available bikes."""
    stations = session.exec(
        select(BikeStation).where(BikeStation.available_bikes >= min_bikes)
    ).all()
    return stations

# Example of a more complex endpoint that updates bike availability
@app.post("/stations/{station_id}/rent")
async def rent_bike(station_id: int, session: Session = Depends(get_session)):
    """Rent a bike from a station, reducing available bikes by 1."""
    station = session.get(BikeStation, station_id)
    if not station:
        raise HTTPException(status_code=404, detail="Station not found")
    
    if station.available_bikes <= 0:
        raise HTTPException(status_code=400, detail="No bikes available at this station")
    
    station.available_bikes -= 1
    station.last_updated = datetime.datetime.now()
    session.add(station)
    session.commit()
    
    return {"message": "Bike rented successfully", "station": station}

@app.post("/stations/{station_id}/return")
async def return_bike(station_id: int, session: Session = Depends(get_session)):
    """Return a bike to a station, increasing available bikes by 1."""
    station = session.get(BikeStation, station_id)
    if not station:
        raise HTTPException(status_code=404, detail="Station not found")
    
    if station.available_bikes >= station.capacity:
        raise HTTPException(status_code=400, detail="Station is at full capacity")
    
    station.available_bikes += 1
    station.last_updated = datetime.datetime.now()
    session.add(station)
    session.commit()
    
    return {"message": "Bike returned successfully", "station": station}
