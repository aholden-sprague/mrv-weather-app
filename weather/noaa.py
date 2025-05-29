import requests
from weather.cache import get_from_cache, set_cache


def fetch_noaa_forecast(lat, lon):

    headers = {
        "User-Agent": "MRV-App/1.0 (aholden@example.com)",
        "Accept": "application/ld+json"
    }

    try:
        key = f'forecast:{lat},{lon}'
        cached = get_from_cache(key, max_age_seconds=1800) #30 min
        if cached:
            return cached
        point_url = f"https://api.weather.gov/points/{lat},{lon}"
        point_res = requests.get(point_url, headers=headers, timeout=10)
        point_res.raise_for_status()
        point_data = point_res.json()

        forecast_url = point_data.get("forecast")
        hourly_url = point_data.get("forecastHourly")

        if not forecast_url or not hourly_url:
            raise Exception("Missing forecast URLs")

        forecast = requests.get(forecast_url, headers=headers, timeout=10).json()
        hourly = requests.get(hourly_url, headers=headers, timeout=10).json()

        set_cache(key, (forecast, hourly))
        return forecast, hourly
    except Exception as e:
        print(f"[ERROR] NOAA forecast fetch failed: {e}")
        return {"properties": {"periods": []}}, {"properties": {"periods": []}}

def fetch_noaa_observations(station, hours=72):
    try:
        key = f'obs:{station}'
        cached = get_from_cache(key, max_age_seconds=1800) #30 min
        if cached:
            return cached
        url = f"https://api.weather.gov/stations/{station}/observations?limit={hours}"
        headers = {"User-Agent": "MRV-App/1.0"}
        res = requests.get(url, headers=headers, timeout=10)
        res.raise_for_status()
        set_cache(key, res.json().get("features", []))
        return res.json().get("features", [])
    except Exception as e:
        print(f"[ERROR] NOAA observations fetch failed: {e}")
        return []
