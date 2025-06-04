# Mad River Valley Weather App
This is a Flask web application that provides weather forecasts, historical snow data, and live webcam views for Sugarbush and Mad River Glen ski resorts in Vermont.

It’s designed for skiers, snowboarders, and outdoor enthusiasts who want accurate, easy-to-read mountain weather information.

# Features
7-Day Forecast Grid (day/night view with icons and tooltips)

48-Hour Hourly Forecast (temperature, wind, conditions, precipitation chance)

Current Conditions (text-based summary with temperature indicators)

Live Webcam Grid (preview images and direct links)

NOAA-integrated forecast and observation data with in-memory caching

Fallback system if NOAA API is unavailable

# Live Demo
Visit: https://mrv-weather-app.onrender.com

# Project Structure
graphql
Copy
Edit
```
mrv-weather-app/
├── app.py                  # Main Flask application
├── requirements.txt        # Python dependencies
├── render.yaml             # Render deployment configuration
│
├── weather/                # Custom logic modules
│   ├── noaa.py             # NOAA forecast and observations
│   ├── summarize.py        # Daily snow and temperature summaries
│   ├── cache.py            # In-memory caching layer
│   ├── mountain_scrape.py  # Infor from mountain reports
│   └── conditions.py       # Text formatting helpers
│
├── templates/              # HTML templates
│   ├── index.html          # Home page with forecast and webcams
│   └── mountain.html       # Individual mountain forecast views
│
├── static/                 # Stylesheets and images
│   ├── style.css
│   ├── sugarbush.png
│   └── mrg.png
```
# Getting Started
1. Clone the repository
bash
Copy
Edit
git clone https://github.com/aholden-sprague/mrv-weather-app.git
cd mrv-weather-app
2. Create a virtual environment and install dependencies
bash
Copy
Edit
python -m venv venv
source venv/bin/activate        # On Windows: venv\Scripts\activate
pip install -r requirements.txt
3. Run the app locally
bash
Copy
Edit
python app.py
Then open your browser to: http://localhost:5000

# Deployment (Render)
This app is preconfigured for deployment to Render:

Push your code to GitHub

Create a new Web Service on Render

Runtime: Python

Build Command: pip install -r requirements.txt

Start Command: gunicorn app:app

(Optional) Use render.yaml for auto-deploys

# Requirements
Flask

Requests

Gunicorn

BeautifulSoup (bs4)

Jinja2

Bootstrap 5 (via CDN)

NOAA Weather API

# Credits
NOAA Weather API – weather.gov

Sugarbush – sugarbush.com

Mad River Glen – madriverglen.com

Bootstrap 5 Icons

# License
MIT License — Free for personal or educational use.

# Author
Created by Andrew Holden

Feedback and contributions welcome.
