from collections import defaultdict

def summarize_observations(observations, days=5):
    daily_data = defaultdict(lambda: {
        "temps": [],
        "snowfall": []
    })

    for obs in observations:
        props = obs["properties"]
        timestamp = props["timestamp"]
        date = timestamp[:10]  # 'YYYY-MM-DD'

        temp_c = props.get("temperature", {}).get("value")
        precip_mm = props.get("precipitationLastHour", {}).get("value")

        # Convert temperature to Fahrenheit
        if temp_c is not None:
            temp_f = (temp_c * 9/5) + 32
            daily_data[date]["temps"].append(temp_f)

        # Convert mm to inches
        if precip_mm is not None:
            snowfall_in = precip_mm / 25.4
            daily_data[date]["snowfall"].append(snowfall_in)

    # Aggregate per day
    summary = []
    for date in sorted(daily_data.keys(), reverse=True)[:days]:
        day = daily_data[date]
        temps = day["temps"]
        snowfall = sum(day["snowfall"])

        summary.append({
            "date": date,
            "min_temp": round(min(temps), 1) if temps else None,
            "max_temp": round(max(temps), 1) if temps else None,
            "snowfall": round(snowfall, 2)
        })

    return summary


def summarize_recent_snowfall(observations, days=3):
    from collections import defaultdict
    daily_snow = defaultdict(float)

    for obs in observations:
        ts = obs["properties"]["timestamp"]
        date = ts[:10]
        mm = obs["properties"].get("precipitationLastHour", {}).get("value")
        if mm is not None:
            daily_snow[date] += mm / 25.4

    totals = sorted(daily_snow.items(), reverse=True)
    return round(sum(s for _, s in totals[:days]), 2)

def summarize_forecast_snowfall(hourly, hours=48):
    total = 0.0
    for h in hourly[:hours]:
        mm = h.get("quantitativePrecipitation", {}).get("value")
        if mm is not None:
            total += mm / 25.4
    return round(total, 2)

def get_current_conditions(observations):
    for obs in observations:
        p = obs["properties"]
        c = p.get("textDescription")
        t = p.get("temperature", {}).get("value")
        if c and t is not None:
            return {"temp": round((t * 9/5) + 32, 1), "condition": c}
    return {"temp": None, "condition": "N/A"}
