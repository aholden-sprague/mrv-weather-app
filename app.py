from flask import Flask, render_template, jsonify
from weather.noaa import fetch_noaa_forecast, fetch_noaa_observations
from weather.summarize import summarize_recent_snowfall, summarize_forecast_snowfall, get_current_conditions, summarize_observations
from weather.conditions import condition_to_emoji, thermometer_emoji
import time

app = Flask(__name__)

weather_cache = {}

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
        "url": "https://www.youtube.com/watch?v=n5QqJSYEZT8"
    },
    {
        "name": "Sugarbush Ellen Base",
        "url": "https://www.youtube.com/watch?v=ipi5Fl4L68c"
    },
    {
        "name": "Sugarbush Allyn's Lodge",
        "url": "https://www.youtube.com/watch?v=SW8uNfI43E4"
    },
    {
        "name": "Mad River Base",
        "url": "https://www.youtube.com/watch?v=wVOqgmbvCrY"
    },
    {
        "name": "Mad River Mid",
        "url": "https://www.youtube.com/watch?v=zMuhC48767w"
    }
    
]




@app.route('/')
def index():
    summaries = {}

    for mountain_id, mtn in LOCATIONS.items():
        forecast, hourly = fetch_noaa_forecast(mtn["lat"], mtn["lon"])
        observations = fetch_noaa_observations(mtn["station"])

        recent_snow = summarize_recent_snowfall(observations)
        forecast_snow = summarize_forecast_snowfall(hourly["periods"])
        current = get_current_conditions(observations)

        summaries[mountain_id] = {
            "name": mtn["name"],
            "icon": mtn["icon"],
            "recent_snow": recent_snow,
            "forecast_snow": forecast_snow,
            "current_temp": current["temp"],
            "condition": current["condition"],
            "condition_emoji": condition_to_emoji(current["condition"]),
            "thermo_emoji": thermometer_emoji(current["temp"])
        }

    return render_template("index.html", summaries=summaries, webcams=WEBCAMS)

# Mountain detail page
@app.route('/mountain/<mountain_id>')
def mountain_page(mountain_id):
    if mountain_id not in LOCATIONS:
        return "Mountain not found", 404

    mtn = LOCATIONS[mountain_id]
    forecast, hourly = fetch_noaa_forecast(mtn["lat"], mtn["lon"])
    observations = fetch_noaa_observations(mtn["station"], hours=25*5)

    # Split into day/night rows
    periods = forecast["periods"]
    days = [p for p in periods if p["isDaytime"]][:7]
    nights = [p for p in periods if not p["isDaytime"]][:7]

    obs_summary = summarize_observations(observations, days=5)
    hourly_forecast = hourly["periods"][:48]

    return render_template(
        "mountain.html",
        mountain=mtn,
        days=days,
        nights=nights,
        hourly=hourly_forecast,
        obs_summary=obs_summary
    )

if __name__ == "__main__":
    app.run(debug=True)
