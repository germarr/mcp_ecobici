import marimo

__generated_with = "0.14.0"
app = marimo.App(width="medium")


@app.cell
def _():
    return


@app.cell
def _():
    import pandas as pd
    import duckdb
    return (duckdb,)


@app.cell
def _():
    import sqlmodel

    DATABASE_URL = "sqlite:///C:/Users/gerym/Documents/mcp/mcp_ecobici/bike_sharing2.db"
    engine = sqlmodel.create_engine(DATABASE_URL)
    return


@app.cell
def _(duckdb):
    path_u = 'C:/Users/gerym/Documents/mcp/mcp_ecobici/notebooks/data/2025_01.parquet'

    duckone_bikes = duckdb.sql(f""" 
    WITH base as (SELECT * 
            EXCLUDE(hora_retiro,hora_arribo), 
            fecha_retiro_completa::TIME as hora_retiro,
            fecha_arribo_completa::TIME as hora_arribo 
            FROM read_parquet("{path_u}") ORDER BY fecha_arribo ASC)

    SELECT fecha_arribo,
        DATE_TRUNC('month', fecha_arribo::DATE) AS first_day_of_month,
        day_of_the_week, 
        SUM(distance_meters)::INTEGER AS distance_meters,
        ROUND(SUM(time_between_trips), 2) AS time_between_trips,
        COUNT(*) AS total_trips 
        FROM base 
        GROUP BY 1, 2, 3 
        ORDER BY fecha_arribo::TIMESTAMP ASC
    """).df()

    duckone_bikes

    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
