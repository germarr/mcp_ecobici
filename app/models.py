"""
Models module for the Ecobici bike-sharing application.
This module contains SQLModel classes used throughout the application.
"""

from sqlmodel import Field, SQLModel
from typing import Optional
import uuid
import datetime

class BikeTrip(SQLModel, table=True):
    """
    Represents a bike trip in the Ecobici system.
    Contains information about the trip, the user, and the stations.
    """
    id: Optional[str] = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True)
    genero_usuario: Optional[str] = Field(default=None)
    edad_usuario: Optional[int] = Field(default=None)
    bici: Optional[str] = Field(default=None)
    ciclo_estacion_retiro: Optional[str] = Field(default=None)
    fecha_retiro: Optional[str] = Field(default=None)
    ciclo_estacionarribo: Optional[str] = Field(default=None)
    fecha_arribo: Optional[str] = Field(default=None)
    fecha_retiro_completa: Optional[str] = Field(default=None)
    fecha_arribo_completa: Optional[str] = Field(default=None)
    time_between_trips: Optional[float] = Field(default=None)
    day_of_the_week: Optional[str] = Field(default=None)
    is_weekend: Optional[int] = Field(default=None)
    lat_start: Optional[float] = Field(default=None)
    lon_start: Optional[float] = Field(default=None)
    lat_end: Optional[float] = Field(default=None)
    lon_end: Optional[float] = Field(default=None)
    distance_meters: Optional[float] = Field(default=None)
    hora_retiro: Optional[str] = Field(default=None)
    hora_arribo: Optional[str] = Field(default=None)

# Define database model
class BikeStation(SQLModel, table=True):
    """
    Represents a bike station in the Ecobici system.
    """
    index: str = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True)
    ciclo_estacionarribo: str
    alcaldia: Optional[str] = Field(default=None)
    colonia: Optional[str] = Field(default=None)
    zip_code: int
    ciclo_estacion_retiro: str