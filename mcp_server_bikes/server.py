# server.py
from mcp.server.fastmcp import FastMCP
import duckdb
import sys
import os
import pandas as pd
from typing import List, Optional
from pydantic import BaseModel

# Add the parent directory to sys.path to import from app module
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Import BikeTrip from app.models
from app.models import BikeTrip
from sqlmodel import Session, create_engine, select

# Import the SQL agent
from agents.sql_agent import agent as sql_agent

# Create an MCP server
mcp = FastMCP("Ecobici Bike-Sharing API")

# @mcp.tool()
# def get_biketrip_columns() -> list[str]:
#     """Return the column names of the BikeTrip table from the SQLite database."""
#     db_path = r"C:/Users/gerym/Documents/mcp/mcp_ecobici/bike_sharing.db"
#     table_name = "bike_trips"
    
#     with duckdb.connect("C:/Users/gerym/Documents/mcp/mcp_ecobici/bike_sharing.db") as con:
#         tables = con.execute("SHOW TABLES").fetchall()
#         print("DuckDB tables:", tables)
    
#     return tables


@mcp.tool()
async def generate_sql_query(user_prompt: str) -> dict:
    """Generate an SQL query string based on the user prompt using the SQL agent."""
    result = await sql_agent.run(user_prompt)
    # The result may be Success or InvalidRequest
    if hasattr(result.output, 'sql_query'):
        # Optionally, you can execute the query with duckdb here if needed
        with duckdb.connect("C:/Users/gerym/Documents/mcp/mcp_ecobici/bike_sharing.db") as con:
            tables = con.execute(result.output.sql_query).df().to_dict('records')

        return {
            'sql_query': result.output.sql_query,
            'explanation': result.output.explanation,
            'result': tables
        }
    else:
        return {'error': getattr(result.output, 'error_message', 'Unknown error')}