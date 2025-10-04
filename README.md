A full-stack web application that provides real-time weather information for cities worldwide with caching capabilities for improved performance.

 Features
Real-time Weather Data: Get current weather conditions for any city

Multi-city Support: Add and monitor multiple cities simultaneously

Intelligent Caching: Redis-based caching to reduce API calls and improve response times

Auto-refresh: Weather data automatically updates every minute

Responsive Design: Clean, user-friendly interface



 Project Structure
text
Real-Time Weather dashboard/
├── flask-server/
│   ├── main.py                 # FastAPI server implementation
│   ├── requirements.txt        # Python dependencies
│   └── .env                   # Environment variables
├── client/
│   └── src/
│       ├── App.js             # Main React component
│       ├── App.css            # Styling for the application
│       ├── index.js           # React entry point
│       └── index.css          # Global styles
├── package.json               # Node.js dependencies
└── README.md                  # This file
Technologies Used
Backend
FastAPI: Modern, fast web framework for building APIs

Redis: In-memory data structure store for caching

Python-dotenv: Environment variable management

Requests: HTTP library for API calls

Uvicorn: ASGI server for running FastAPI

Frontend
React: JavaScript library for building user interfaces

Axios: Promise-based HTTP client for API requests

CSS3: Styling and responsive design

External Services
OpenWeatherMap API: Source of weather data

 Prerequisites
Before running this application, ensure you have the following installed:

Node.js (v14 or higher)

Python (v3.8 or higher)

Redis server

OpenWeatherMap API account 

 Installation & Setup

Backend Setup

bash
cd flask-server

# Create virtual environment
python -m venv venv

# Activate virtual environment

venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env with your actual values:
# OPENWEATHER_API_KEY=your_openweather_api_key_here
# REDIS_HOST=localhost
# REDIS_PORT=6379
# REDIS_DB=0
# CACHE_EXPIRY=300
Frontend Setup

bash
cd ../client

# Install dependencies
npm install
Start Redis Server


# Download and install Redis from https://github.com/microsoftarchive/redis/releases
Running the Application
Start the Backend Server

bash
cd backend
# Make sure your virtual environment is activated
python main.py
The API will be available at http://localhost:8000

Start the Frontend Development Server

bash
cd client
npm start
The application will be available at http://localhost:3000


Open your browser and navigate to http://localhost:3000

Enter a city name in the input field and click "Add City"

View current weather information including temperature, humidity, wind speed, and conditions

The "Cached" indicator shows when data is being served from cache

Add multiple cities to monitor their weather simultaneously

Remove cities by clicking the "Remove" button on any weather card

Configuration
The application can be configured through environment variables:

OPENWEATHER_API_KEY: Your OpenWeatherMap API key (required)

REDIS_HOST: Redis server hostname (default: localhost)

REDIS_PORT: Redis server port (default: 6379)

REDIS_DB: Redis database number (default: 0)

CACHE_EXPIRY: Cache expiration time in seconds (default: 300)



Troubleshooting
API Key Issues: Ensure you have a valid OpenWeatherMap API key set in your .env file

Redis Connection Errors: Verify that Redis server is running and accessible

CORS Errors: Ensure the frontend is running on http://localhost:3000


Fork the repository

Create a feature branch (git checkout -b feature)

Commit your changes (git commit -m 'Add some  feature')

Push to the branch (git push origin feature)

Open a Pull Request

License
This project is licensed under the MIT License - see the LICENSE file for details.

Acknowledgments
Weather data provided by OpenWeatherMap



