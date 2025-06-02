from flask import Flask, render_template, jsonify
from weather.noaa import fetch_noaa_forecast, fetch_noaa_observations
from weather.summarize import summarize_recent_snowfall, summarize_forecast_snowfall, get_current_conditions, summarize_observations
from weather.conditions import condition_to_emoji, thermometer_emoji
from weather.mountain_scrape import get_current_obs
import time
from datetime import datetime, timedelta

app = Flask(__name__)

LOCATIONS = {
    'ellen_summit': {'lat':44.16048, 'lon':-72.9292, 'elevation':4050, 'station': 'KBTV', 'icon': 'sugarbush.png', 'name': 'Mt. Ellen'},
    'lincoln_summit': {'lat':44.12774, 'lon':-72.92815, 'elevation':3900, 'station': 'KBTV', 'icon': 'sugarbush.png', 'name': 'Lincoln Peak'},
    'mrg_summit': {'lat':44.19187, 'lon':-72.93147, 'elevation':3630, 'station': 'KBTV', 'icon': 'mrg.png', 'name': 'Mad River Glen'}
    #'ellen_base': {'lat':44.17727, 'lon':-72.90073, 'elevation':1540, 'station': 'KBTV', 'icon': 'sugarbush.png', 'name': 'Mt. Ellen Base'},
    #'lincoln_base': {'lat':44.13535, 'lon':-72.89608, 'elevation':1600, 'station': 'KBTV', 'icon': 'sugarbush.png', 'name': 'Lincoln Peak Base'},
    #'mrg_base': {'lat':44.20238, 'lon':-72.91631, 'elevation':1640, 'station': 'KBTV', 'icon': 'mrg.png', 'name': 'MRG Base'}
    
}

WEBCAMS = [
    {
        "name": "Sugarbush Super Bravo",
        "url": "https://www.youtube.com/embed/n5QqJSYEZT8"
    },
    {
        "name": "Sugarbush Ellen Base",
        "url": "https://www.youtube.com/embed/ipi5Fl4L68c"
    },
    {
        "name": "Sugarbush Allyn's Lodge",
        "url": "https://www.youtube.com/embed/SW8uNfI43E4"
    },
    {
        "name": "Mad River Base",
        "url": "https://www.youtube.com/embed/wVOqgmbvCrY"
    },
    {
        "name": "Mad River Mid",
        "url": "https://www.youtube.com/embed/zMuhC48767w"
    }
    
]




@app.route('/')
def index():
    summaries = {}

    for mountain_id, mtn in LOCATIONS.items():
        #lat, lon, elev = mtn["lat"], mtn["lon"], mtn["elevation"]
        #today = datetime.today()
        #start = today - timedelta(days=5)
        #history = fetch_open_meteo_history(lat, lon, elev)

        #forecast, hourly = fetch_noaa_forecast(mtn["lat"], mtn["lon"])
        #observations = fetch_noaa_observations(mtn["station"])
        observations = get_current_obs(mtn['name'])


        summaries[mountain_id] = {
            "name": mtn["name"],
            "icon": mtn["icon"],
            "past_snow": observations['past_snow'],
            "forecast_snow": observations['forecast_snow'],
            "current_temp": observations['current_temp'],
            "condition": observations["condition"],
            "recent_snow": observations['recent_snow'],
            "condition_emoji": condition_to_emoji(observations["condition"]),
            "thermo_emoji": thermometer_emoji(observations["current_temp"]),
            "wind": observations['wind']
        }

    return render_template("index.html", summaries=summaries, webcams=WEBCAMS)

# Mountain detail page
@app.route('/mountain/<mountain_id>')
def mountain_page(mountain_id):
    if mountain_id not in LOCATIONS:
        return "Mountain not found", 404

    mtn = LOCATIONS[mountain_id]
    lat, lon, elev = mtn["lat"], mtn["lon"], mtn["elevation"]

    today = datetime.today()
    start = today - timedelta(days=5)
    forecast, hourly = fetch_noaa_forecast(mtn["lat"], mtn["lon"])
    observations = fetch_noaa_observations(mtn["station"], hours=25*5)

    # Split into day/night rows
    periods = forecast["periods"]
    days = [p for p in periods if p["isDaytime"]][:7]
    nights = [p for p in periods if not p["isDaytime"]][:7]

    #obs_summary = summarize_observations(observations, days=5)
    hourly_forecast = hourly["periods"][:48]

    return render_template(
        "mountain.html",
        mountain=mtn,
        days=days,
        nights=nights,
        hourly=hourly_forecast
    )

if __name__ == "__main__":
    app.run(debug=True)
