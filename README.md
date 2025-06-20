# 🚲 Ecobici Data Platform

A modern, extensible platform for managing, analyzing, and serving data from the Ecobici bike-sharing program. Built with FastAPI, SQLModel, DuckDB, and a custom MCP (Model Context Protocol) server with OpenAI-powered SQL generation.

---

## 📦 Project Structure

- **app/**: FastAPI web app, database models, and API endpoints
- **mcp_server_bikes/**: MCP server exposing tools/resources for data and AI-powered SQL
- **agents/**: AI agent for generating SQL queries from natural language
- **notebooks/**: Jupyter notebooks for data exploration and analysis
- **bike_sharing.db**: SQLite database with bike trip and station data

## ✨ Features

- 🔗 **REST API** for bike stations and trip management (CRUD, search, rent/return, etc.)
- 🖥️ **Landing Page** with Jinja2, HTML, CSS, and JS (see `/`)
- 📊 **Jupyter Notebooks** for advanced analytics and visualization
- 🤖 **MCP Server** with:
  - Tools for database schema inspection
  - Tools for running DuckDB queries
  - Integration with an OpenAI-powered agent that generates SQL from user prompts
- 🗃️ **Unified Data Model** using SQLModel and Pydantic
- 🦆 **DuckDB** for fast analytics on SQLite and Parquet data

## 🛠️ Tech Stack

- **Backend**: FastAPI, SQLModel, DuckDB, SQLite
- **AI/Agent**: OpenAI (via pydantic_ai), custom SQL agent
- **Frontend**: Jinja2, HTML5, CSS3, JavaScript
- **Data Science**: Jupyter, Pandas, Seaborn, Matplotlib
- **MCP**: Model Context Protocol server for tool/resource orchestration

## 🚀 Quickstart

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd mcp_ecobici
   ```
2. **Set up your Python environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -e .
   ```
3. **Add your OpenAI key**
   - Create a `.env` file in the root folder:
     ```
     openaikey=sk-...
     ```
4. **Run the FastAPI app**
   ```bash
   uvicorn app.main:app --reload
   ```
   - Visit [http://localhost:8000](http://localhost:8000) for the landing page
   - Visit [http://localhost:8000/docs](http://localhost:8000/docs) for the API docs
5. **Run the MCP server**
   ```bash
   python mcp_server_bikes/server.py
   ```
6. **Explore the Jupyter notebooks**
   ```bash
   jupyter lab
   # Open notebooks/send_bikes.ipynb
   ```

## 🧩 Key Components

- **API Endpoints**: CRUD for stations, trip analytics, and more
- **MCP Tools**:
  - `get_biketrip_columns`: List columns in the bike trips table
  - `generate_sql_query`: Use natural language to generate SQL (via OpenAI agent)
- **SQL Agent**: Converts user prompts to SQL queries using OpenAI (see `agents/sql_agent.py`)
- **Data Analysis**: Notebooks for ETL, stats, and visualization

## 📚 Example Usage

- **Generate SQL from a prompt** (via MCP):
  ```python
  # In MCP tool or Python
  result = generate_sql_query("show me the total trips by gender")
  print(result['sql_query'])
  ```
- **Analyze trip data in a notebook**:
  ```python
  import duckdb
  with duckdb.connect("bike_sharing.db") as con:
      df = con.execute("SELECT * FROM bike_trips LIMIT 10").df()
  ```

## 📝 Notebooks

- `send_bikes.ipynb`: Data loading, transformation, and analytics (DuckDB, Pandas, Seaborn)

## 🧠 AI Integration

- **Natural Language to SQL**: The agent in `agents/sql_agent.py` uses OpenAI to turn user requests into SQL queries for the Ecobici schema.
- **.env**: Place your OpenAI key as `openaikey=...` in the root `.env` file.

## 🏗️ Extending

- Add new MCP tools/resources in `mcp_server_bikes/server.py`
- Add new models in `app/models.py`
- Add new notebooks in `notebooks/`

## 📄 License

See LICENSE file.

---

Made with ❤️ for open data and urban mobility | Last updated: June 19, 2025
