// Main JavaScript for Ecobici Bike-Sharing App

document.addEventListener('DOMContentLoaded', function() {
    // DOM Elements
    const stationsBtn = document.getElementById('stationsBtn');
    const stationsSection = document.getElementById('stations-section');
    const stationsList = document.getElementById('stations-list');
    
    // Toggle stations section visibility
    stationsBtn.addEventListener('click', function() {
        if (stationsSection.style.display === 'none') {
            stationsSection.style.display = 'block';
            loadStations();
            stationsBtn.innerHTML = '<i class="fas fa-chevron-up"></i> Hide Stations';
        } else {
            stationsSection.style.display = 'none';
            stationsBtn.innerHTML = '<i class="fas fa-map-marker-alt"></i> View Stations';
        }
    });
    
    // Load stations from API
    async function loadStations() {
        try {
            stationsList.innerHTML = '<div class="loading">Loading stations...</div>';
            
            const response = await fetch('/stations/');
            
            if (!response.ok) {
                throw new Error(`HTTP error! Status: ${response.status}`);
            }
            
            const stations = await response.json();
            
            if (stations.length === 0) {
                stationsList.innerHTML = '<div class="loading">No stations available</div>';
                return;
            }
            
            displayStations(stations);
        } catch (error) {
            console.error('Error loading stations:', error);
            stationsList.innerHTML = `<div class="loading">Error loading stations: ${error.message}</div>`;
        }
    }
    
    // Display stations in the DOM
    function displayStations(stations) {
        stationsList.innerHTML = '';
        
        stations.forEach(station => {
            // Determine bike availability class
            let availabilityClass = 'bikes-available';
            if (station.available_bikes === 0) {
                availabilityClass = 'bikes-none';
            } else if (station.available_bikes < 5) {
                availabilityClass = 'bikes-low';
            }
            
            // Format last updated time
            const lastUpdated = new Date(station.last_updated);
            const formattedDate = lastUpdated.toLocaleString();
            
            // Create station card HTML
            const stationCard = document.createElement('div');
            stationCard.className = 'station-card';
            stationCard.innerHTML = `
                <h3 class="station-name">${station.name}</h3>
                <p class="station-details">Location: ${station.location}</p>
                <p class="station-details">Capacity: ${station.capacity} bikes</p>
                <p class="station-details">
                    Available bikes: 
                    <span class="${availabilityClass}">${station.available_bikes}</span>
                </p>
                <p class="station-details">Last updated: ${formattedDate}</p>
            `;
            
            stationsList.appendChild(stationCard);
        });
    }
});
