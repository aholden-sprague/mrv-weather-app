def condition_to_emoji(condition):
    cond = condition.lower()
    if "snow" in cond:
        return "🌨️"
    elif "rain" in cond or "shower" in cond:
        return "🌧️"
    elif "cloud" in cond or "overcast" in cond:
        return "☁️"
    elif "sun" in cond or "clear" in cond:
        return "☀️"
    elif "fog" in cond:
        return "🌫️"
    else:
        return "🌤️"

def thermometer_emoji(temp):
    if temp is None:
        return "🌡️"
    if temp <= 10:
        return "🥶"
    elif temp <= 32:
        return "❄️"
    else:
        return "🌡️"
