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
    import uuid
    return duckdb, uuid


@app.cell
def _(duckdb):
    con = duckdb.connect('C:/Users/gerym/Documents/mcp/mcp_ecobici/ecobici.duckdb')
    return (con,)


@app.cell
def _(duckdb):
    fileFolder = 'D:/Ecobici/CLEAN'

    # testDataset = duckdb.sql(f""" 
    # SELECT * FROM read_parquet(['{fileFolder}/2025_01.parquet'])
    # """)

    rides_all = duckdb.sql(f""" 
    SELECT * EXCLUDE(fecha_retiro,fecha_arribo),fecha_retiro_completa::date AS fecha_retiro,fecha_arribo_completa::date AS fecha_arribo   
        FROM read_parquet(['{fileFolder}/2025/*.parquet',
        '{fileFolder}/2024/*.parquet',
        '{fileFolder}/2023/*.parquet',
        '{fileFolder}/2022/*.parquet',
        '{fileFolder}/2021/*.parquet',
        '{fileFolder}/2020/*.parquet',
        '{fileFolder}/2019/*.parquet',
        '{fileFolder}/2018/*.parquet',
        '{fileFolder}/2017/*.parquet']) 
    """)
    return (rides_all,)


@app.cell
def _(duckdb):
    stations = duckdb.sql(f"""SELECT * FROM read_csv('D:\Ecobici\stations_alcaldias_colonias_zips.csv')""").df()
    return (stations,)


@app.cell
def _(stations, uuid):
    stations['index'] = [str(uuid.uuid4()) for _ in range(len(stations))]
    stations['ciclo_estacion_retiro'] = stations['ciclo_estacionarribo']
    return


@app.cell
def _(stations):
    stations.head(3)
    return


@app.cell
def _(con):
    con.execute(f"""
    CREATE OR REPLACE TABLE stations AS 
    SELECT * FROM stations
    """)
    return


@app.cell
def _(duckdb, rides_all):
    duckone_bikes = duckdb.sql(f""" 
    WITH base as (SELECT * 
            EXCLUDE(hora_retiro,hora_arribo), 
            fecha_retiro_completa::TIME as hora_retiro,
            fecha_arribo_completa::TIME as hora_arribo 
            FROM rides_all ORDER BY fecha_arribo ASC)

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

    return


@app.cell
def _(con):
    con.execute(f"""
    CREATE OR REPLACE TABLE duckone_bikes AS 
    SELECT * FROM duckone_bikes
    """)
    return


@app.cell
def _(con):
    con.execute("""SELECT * FROM duckone_bikes""").df().dtypes
    return


@app.cell
def _(con):
    con.execute("""
        SELECT *, 
               DATE_TRUNC('month', fecha_arribo)::DATE AS first_day_of_month, 
               EXTRACT(month FROM fecha_arribo) AS month, 
               EXTRACT(year FROM fecha_arribo) AS year
        FROM duckone_bikes 
        LIMIT 10
    """).df()

    return


@app.cell
def _(con):
    con.execute("""
        SELECT *, 
               DATE_TRUNC('month', fecha_arribo)::DATE AS first_day_of_month, 
               EXTRACT(month FROM fecha_arribo) AS month, 
               EXTRACT(year FROM fecha_arribo) AS year
        FROM stations 
        LIMIT 10
    """).df()
    return


if __name__ == "__main__":
    app.run()
