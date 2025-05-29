# ❄️ Mad River Valley Weather App 🏔️

This is a Flask web application that provides weather forecasts, historical snow data, and live webcam views for Sugarbush and Mad River Glen ski resorts in Vermont.

The app is built to serve skiers, snowboarders, and outdoor enthusiasts who want clear, reliable, and visual mountain weather info in one place.

---

## 🔧 Features

- 🗓️ **7-Day Forecast Grid** (with Day/Night rows, icons, and tooltips)
- 🕘 **48-Hour Hourly Forecast** (temp, wind, conditions, precip chance)
- ❄️ **Past 5-Day Observations** (min/max temp + snowfall)
- 🌤️ **Current Conditions** with emoji icons and thermometer indicators
- 📷 **Live Webcam Grid** with preview images and links
- 🧠 NOAA-integrated forecasts + in-memory caching
- 💥 Graceful fallback if NOAA API is unavailable

---

## 🌐 Live Demo

📍 [https://your-app-name.onrender.com](https://your-app-name.onrender.com)  
*(Replace with your actual URL once deployed)*

---

## 📁 Project Structure

mrv-weather-app/
│
├── app.py # Main Flask application
├── requirements.txt # Python dependencies
├── render.yaml # Render deployment config
│
├── weather/ # Custom logic modules
│ ├── noaa.py # NOAA forecast + observations
│ ├── summarize.py # Daily snow/temp summaries
│ ├── cache.py # In-memory caching layer
│ └── conditions.py # Emoji + formatting helpers
│
├── templates/ # Jinja2 templates
│ ├── index.html # Home with forecast + webcams
│ └── mountain.html # Per-mountain detailed forecast
│
├── static/ # CSS + images
│ ├── style.css
│ ├── sugarbush.png
│ └── mrg.png

yaml
Copy
Edit

---

## 🚀 Getting Started

### 1. Clone this repo

```bash
git clone https://github.com/yourusername/mrv-weather-app.git
cd mrv-weather-app
2. Create a virtual environment and install dependencies
bash
Copy
Edit
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
3. Run the app locally
bash
Copy
Edit
python app.py
Then visit: http://localhost:5000

🌍 Deployment (Render)
This app is preconfigured for deployment to Render:

1. Push your code to GitHub
2. Create a new Web Service on Render
Runtime: Python

Build Command: pip install -r requirements.txt

Start Command: gunicorn app:app

3. Or use render.yaml for auto-deploys
📦 Requirements
Flask

Requests

Gunicorn

Jinja2

Bootstrap 5 (via CDN)

NOAA Weather API

🧊 Credits
NOAA Weather API – weather.gov

Sugarbush – sugarbush.com

Mad River Glen – madriverglen.com

Icons by Bootstrap + emoji magic 🌨️

🪪 License
MIT License — free for personal or educational use.

🙋‍♂️ Author
Made with ❤️ by Andrew Holden
Feedback or contributions welcome!