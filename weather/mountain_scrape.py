import requests
from bs4 import BeautifulSoup
from weather.cache import get_from_cache, set_cache

def get_sugarbush_weather():
    cache_key = "sugarbush_weather"
    cached = get_from_cache(cache_key, 900)  # 15 minutes
    if cached:
        return cached

    url = "https://mtnpowder.com/feed"
    token = "YOUR_VALID_BEARER_TOKEN"

    try:
        res = requests.get(f"{url}")
        res.raise_for_status()
        data = res.json()
        resorts = data.get("Resorts", [])
        sugarbush = next((r for r in resorts if r.get("Name") == "Sugarbush"), None)

        snow = sugarbush["SnowReport"]["SummitArea"]
        current = sugarbush['CurrentConditions']['Summit']
        forecast = sugarbush["Forecast"]

        result = {
            "snow_24h": int(snow["Last24HoursIn"]),
            "snow_48h": int(snow["Last48HoursIn"]),
            "snow_72h": int(snow["Last72HoursIn"]),
            "f_snow_24h": int(forecast['OneDay']["forecasted_snow_in"]),
            "f_sky_24h": forecast['OneDay']["skies"],
            "f_snow_48h": int(forecast['TwoDay']["forecasted_snow_in"]),
            "f_sky_48h": forecast['TwoDay']["skies"],
            "f_snow_72h": int(forecast['ThreeDay']["forecasted_snow_in"]),
            "f_sky_72h": forecast['ThreeDay']["skies"],
            "current_wind": current["WindStrengthMph"],
            "current_temp": current["TemperatureF"],
            "conditions": current["Skies"]
        }

        set_cache(cache_key, result)
        return result

    except Exception as e:
        print(f"[ERROR] Failed to fetch Sugarbush data: {e}")
        return {}

    
def get_mrg_snow():
    cache_key = "mrg_snow"
    cached = get_from_cache(cache_key, 900)
    if cached:
        return cached

    url = "https://www.madriverglen.com/conditions/"
    headers = {"User-Agent": "MRV Weather App"}

    try:
        res = requests.get(url, headers=headers, timeout=10)
        res.raise_for_status()
        soup = BeautifulSoup(res.text, "html.parser")

        report_data = {}
        for row in soup.find_all("tr"):
            td = row.find("td")
            if td:
                span = td.find("span")
                if span:
                    label_parts = td.contents
                    label_text = ""
                    for part in label_parts:
                        if part.name == "span":
                            break
                        label_text += str(part).strip()
                    label = label_text.rstrip(":").strip()
                    value = span.get_text(strip=True)
                    report_data[label] = value

        result = {
            "snow_24h": report_data.get("New Snow", "?")
        }

        set_cache(cache_key, result)
        return result

    except Exception as e:
        print(f"[ERROR] Failed to scrape MRG conditions: {e}")
        return {}

    
def get_mrg_current():
    cache_key = "mrg_current_weather"
    cached = get_from_cache(cache_key, 300)  # shorter cache for live data
    if cached:
        return cached

    url = "https://www.rainwise.net/data/rwxml.php?mac=00C033F798DC&json=1"
    headers = {"User-Agent": "MRV Weather App"}

    try:
        res = requests.get(url, headers=headers, timeout=10)
        res.raise_for_status()
        data = res.json()

        weather = {
            "current_temp": data.get("temp_f", "?"),
            "current_wind": data.get("wind_mph", "?")
        }

        set_cache(cache_key, weather)
        return weather

    except Exception as e:
        print(f"[ERROR] Failed to fetch MRG RainWise JSON: {e}")
        return {}

    
def get_current_obs(mountain):
    sb = get_sugarbush_weather()
    mrg_snow = get_mrg_snow()
    mrg_curr = get_mrg_current()

    forecast_snow = sb['f_snow_24h'] + sb['f_snow_48h']
    past_snow = sb['snow_24h'] + sb['snow_48h'] + sb['snow_72h']
    condition = sb['conditions']

    if mountain == 'Mad River Glen':
        curr_temp = mrg_curr['current_temp']
        recent_snow = mrg_snow['snow_24h'].split('-')[-1]
        wind = mrg_curr['current_wind']
    else:
        curr_temp = sb['current_temp']
        recent_snow = str(sb['snow_24h']) + '"'
        wind = sb['current_wind']

    return {
        'forecast_snow': forecast_snow,
        'past_snow': past_snow,
        'condition': condition,
        'current_temp': float(curr_temp),
        'recent_snow': recent_snow,
        'wind': wind
    }
