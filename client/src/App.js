import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './App.css';

function App() {
  const [cities, setCities] = useState([]);
  const [weatherData, setWeatherData] = useState({});
  const [newCity, setNewCity] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const fetchWeather = async (city) => {
    try {
      const response = await axios.get(`http://localhost:8000/weather/${city}`);
      return { [city.toLowerCase()]: response.data };
    } catch (err) {
      console.error(`Error fetching weather for ${city}:`, err);
      setError(`Failed to fetch weather for ${city}. Please check the city name.`);
      return null;
    }
  };

  const updateAllWeather = async () => {
    if (cities.length === 0) return;
    
    setLoading(true);
    const promises = cities.map(city => fetchWeather(city));
    const results = await Promise.all(promises);
    const newData = results.reduce((acc, curr) => {
      if (curr) return { ...acc, ...curr };
      return acc;
    }, {});
    
    setWeatherData(prev => ({ ...prev, ...newData }));
    setLoading(false);
  };
  const refreshCity =  () => {
        
  }
  useEffect(() => {
    if (cities.length > 0) {
      updateAllWeather();
      const interval = setInterval(updateAllWeather, 60000); // Update every minute
      return () => clearInterval(interval);
    }
  }, [cities]);

  const addCity = async () => {
    if (!newCity.trim()) {
      setError('Please enter a city name');
      return;
    }
    
    const normalized = newCity.trim().toLowerCase();
    if (cities.some(c => c.toLowerCase() === normalized)) {
      setError('City already added');
      return;
    }
    
    setError('');
    setLoading(true);
    
    try {
      
      const response = await axios.get(`http://localhost:8000/weather/${newCity.trim()}`);
      
      
      setCities(prev => [...prev, newCity.trim()]);
      setWeatherData(prev => ({
        ...prev, 
        [normalized]: response.data
      }));
      setNewCity('');
    } catch (err) {
      setError('City not found. Please check the spelling.');
      console.error('Error adding city:', err);
    } finally {
      setLoading(false);
    }
  };

  const removeCity = (city) => {
    setCities(prev => prev.filter(c => c.toLowerCase() !== city.toLowerCase()));
    setWeatherData(prev => {
      const newData = { ...prev };
      delete newData[city.toLowerCase()];
      return newData;
    });
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter') {
      addCity();
    }
  };

  return (
    <div className="App">
      <h1>Real-Time Weather Dashboard</h1>
      
      <div className="add-city">
        <input
          type="text"
          value={newCity}
          onChange={(e) => setNewCity(e.target.value)}
          onKeyPress={handleKeyPress}
          placeholder="Enter city name"
          disabled={loading}
        />
        <button onClick={addCity} disabled={loading}>
          {loading ? 'Adding...' : 'Add City'}
        </button>
        {error && <p className="error">{error}</p>}
      </div>
      
      <div className="dashboard">
        {cities.length === 0 ? (
          <p className="no-cities">No cities added yet. Start by adding a city above.</p>
        ) : (
          cities.map(city => {
            const data = weatherData[city.toLowerCase()];
            return (
              <div key={city} className="weather-card">
                <h2>{city}</h2>
                {data ? (
                  <>
                    <div className="weather-main">
                      <p className="temperature">{data.temperature}°C</p>
                      <p className="feels-like">Feels like: {data.feels_like}°C</p>
                    </div>
                    <div className="weather-details">
                      <p>Humidity: {data.humidity}%</p>
                      <p>Condition: {data.description}</p>
                      <p>Wind: {data.wind_speed} m/s</p>
                      <p>Country: {data.country}</p>
                      {data.cached && <span className="cached-indicator">Cached</span>}
                      <button onClick={refreshCity}>referesh </button>
                    </div>
                  </>
                ) : (
                  <p>Loading weather data...</p>
                )}
                <button 
                  onClick={() => removeCity(city)} 
                  className="remove-btn"
                >
                  Remove
                </button>
              </div>
            );
          })
        )}
      </div>
    </div>
  );
}

export default App;