import xml.etree.ElementTree as ET

import requests


def get_weather_data(city):
    try:
        url = f"https://weather.service.msn.com/data.aspx?weasearchstr={city}&culture=en-US&weadegreetype=C&src=outlook"
        response = requests.get(url)
        response.raise_for_status()
        return response.text
    except requests.RequestException as e:
        print(f"Error fetching data for {city} from the weather service: {e}")
        raise


def parse_weather_data(xml_data):
    try:
        root = ET.fromstring(xml_data)
        weather_data = []

        for weather in root.findall("weather"):
            location_data = extract_location_data(weather)
            current_data = extract_current_data(weather)
            forecasts = extract_forecasts(weather)

            location_data["current"] = current_data
            location_data["forecast"] = forecasts
            weather_data.append(location_data)

        return weather_data
    except Exception as e:
        print(f"Error parsing weather data: {e}")
        raise


def extract_location_data(weather):
    location = {}
    for key in [
        "weatherlocationname",
        "lat",
        "long",
        "timezone",
        "alert",
        "degreetype",
        "imagerelativeurl",
    ]:
        if key == "weatherlocationname":
            location["name"] = weather.get(key)
        else:
            location[key] = weather.get(key)
    return {"location": location}


def extract_forecasts(weather):
    forecasts = []
    for forecast in weather.findall("forecast"):
        forecast_data = {}
        for key in [
            "low",
            "high",
            "skycodeday",
            "skytextday",
            "date",
            "day",
            "shortday",
            "precip",
        ]:
            forecast_data[key] = forecast.get(key)
        forecasts.append(forecast_data)
    return forecasts


def extract_current_data(weather):
    current = weather.find("current")
    current_data = {}
    if current is not None:
        for key in [
            "temperature",
            "skycode",
            "skytext",
            "date",
            "observationtime",
            "observationpoint",
            "feelslike",
            "humidity",
            "winddisplay",
            "day",
            "shortday",
            "windspeed",
        ]:
            current_data[key] = current.get(key)

        image_relative_url = weather.get("imagerelativeurl")
        sky_code = current_data.get("skycode")
        if image_relative_url and sky_code:
            current_data["imageUrl"] = f"{image_relative_url}law/{sky_code}.gif"

    return current_data


def get(query):
    xml_data = get_weather_data(query)
    weather_data = parse_weather_data(xml_data)
    return weather_data
