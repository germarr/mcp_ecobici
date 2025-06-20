# 🚲💥 Ecobici Data Platform: Ride the Data Revolution

Welcome to the **Ecobici Data Platform**—where urban mobility meets bleeding-edge analytics, AI, and a dash of chaos. This isn’t your grandma’s bike-sharing dashboard. It’s a full-stack, AI-powered, open-data playground for hackers, data scientists, and city dreamers. 

---

## 🧨 Project Structure

- `app/` — FastAPI web app, SQLModel data models, and REST endpoints
- `mcp_server_bikes/` — Model Context Protocol (MCP) server: tools, AI, and SQL magic
- `agents/` — OpenAI-powered agent that turns your wildest questions into SQL
- `notebooks/` — Jupyter notebooks for data wrangling, stats, and wild visualizations
- `bike_sharing.db` — SQLite database: all the trips, all the stations, all the secrets

## ⚡ Features

- 🔗 **REST API**: CRUD for stations, trip analytics, rent/return, and more
- 🖥️ **Landing Page**: Jinja2, HTML, CSS, JS—old school meets new school
- 📊 **Jupyter Notebooks**: For the data scientist in you
- 🤖 **MCP Server**:
  - Schema inspection tools
  - DuckDB query runner
  - OpenAI agent for natural language SQL (ask it anything!)
- 🗃️ **Unified Data Model**: SQLModel + Pydantic = ❤️
- 🦆 **DuckDB**: Analytics at warp speed (on SQLite & Parquet)

## 🛠️ Tech Stack

- **Backend**: FastAPI, SQLModel, DuckDB, SQLite
- **AI/Agent**: OpenAI (via pydantic_ai), custom SQL agent
- **Frontend**: Jinja2, HTML5, CSS3, JavaScript
- **Data Science**: Jupyter, Pandas, Seaborn, Matplotlib
- **MCP**: Model Context Protocol server for tool orchestration

## 🚀 Quickstart

1. **Clone this beast**
   ```bash
   git clone <your-repo-url>
   cd mcp_ecobici
   ```
2. **Summon your Python environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -e .
   ```
3. **Feed the AI**
   - Create a `.env` file in the root:
     ```
     openaikey=sk-...
     ```
4. **Unleash the FastAPI app**
   ```bash
   uvicorn app.main:app --reload
   ```
   - [http://localhost:8000](http://localhost:8000) — landing page
   - [http://localhost:8000/docs](http://localhost:8000/docs) — API docs
5. **Fire up the MCP server**
   ```bash
   python mcp_server_bikes/server.py
   ```
6. **Hack the data in Jupyter**
   ```bash
   jupyter lab
   # Open notebooks/send_bikes.ipynb
   ```

## 🧩 Key Components

- **API Endpoints**: CRUD for stations, trip analytics, and more
- **MCP Tools**:
  - `get_biketrip_columns`: List columns in the bike trips table
  - `generate_sql_query`: Turn natural language into SQL (OpenAI agent)
- **SQL Agent**: Converts your questions into SQL (see `agents/sql_agent.py`)
- **Data Analysis**: Notebooks for ETL, stats, and wild visualizations

## 🧠 AI Integration

- **Natural Language to SQL**: The agent in `agents/sql_agent.py` uses OpenAI to turn your requests into SQL for the Ecobici schema.
- **.env**: Place your OpenAI key as `openaikey=...` in the root `.env` file.

## 📝 Notebooks

- `send_bikes.ipynb`: Data loading, transformation, analytics, and chaos (DuckDB, Pandas, Seaborn)

## 🏗️ Extending the Madness

- Add new MCP tools/resources in `mcp_server_bikes/server.py`
- Add new models in `app/models.py`
- Add new notebooks in `notebooks/`

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

## 📄 License

MIT. Use it, break it, fork it, improve it. Just don’t be evil.

---

Made with ❤️, caffeine, and a little bit of anarchy | Last updated: June 20, 2025
