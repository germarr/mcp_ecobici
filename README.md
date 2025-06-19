# 🚲 Ecobici API & Dashboard

A modern, full-featured API and dashboard for the Ecobici bike-sharing program, built with FastAPI and SQLite.

## 📋 Overview

This project provides a comprehensive solution for managing and visualizing data from the Ecobici bike-sharing program. It features a RESTful API for programmatic access and a clean, intuitive web interface for end users.

## ✨ Features

- 🔄 **Real-time Bike Station Tracking**: Monitor bike availability across multiple stations
- 🌐 **Interactive Web Dashboard**: User-friendly interface built with modern HTML, CSS, and JavaScript
- 📱 **RESTful API**: Complete API for programmatic access to bike-sharing data
- 📊 **Data Analysis**: Jupyter notebooks for exploring and analyzing bike usage patterns
- 🗄️ **SQLite Database**: Lightweight, serverless database solution for storing bike station information

## 🛠️ Tech Stack

- **Backend**: FastAPI, SQLModel, Uvicorn
- **Frontend**: HTML5, CSS3, JavaScript
- **Templates**: Jinja2
- **Database**: SQLite
- **Data Analysis**: Jupyter, Pandas
- **Deployment**: Containerized with Docker (optional)

## 🚀 Getting Started

### Prerequisites

- Python 3.10 or higher
- Pip package manager

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/your-username/mcp_ecobici.git
   cd mcp_ecobici
   ```

2. **Install dependencies**
   ```bash
   pip install -e .
   ```
   
   Or with a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -e .
   ```

3. **Run the application**
   ```bash
   uvicorn app.main:app --reload
   ```

4. **Access the application**
   - Web Interface: http://localhost:8000
   - API Documentation: http://localhost:8000/docs
   - Alternative API Docs: http://localhost:8000/redoc

## 📚 API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Landing page for the web interface |
| `/stations/` | GET | List all bike stations |
| `/stations/{station_id}` | GET | Get details for a specific station |
| `/stations/` | POST | Create a new bike station |
| `/stations/{station_id}` | PUT | Update an existing station |
| `/stations/{station_id}` | DELETE | Remove a station |
| `/stations/available` | GET | Get stations with available bikes |
| `/stations/{station_id}/rent` | POST | Rent a bike from a station |
| `/stations/{station_id}/return` | POST | Return a bike to a station |

## 📊 Data Analysis

The `notebooks/` directory contains Jupyter notebooks for data analysis:

- `send_bikes.ipynb`: Analysis of bike distribution and optimization

## 🔧 Configuration

The application uses SQLite by default. The database will be created automatically when you first run the application.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is licensed under the terms of the included LICENSE file.

## 📞 Contact

For questions or support, please open an issue in the GitHub repository.

---

Made with ❤️ for bike enthusiasts everywhere | Last updated: June 19, 2025
