import json

import requests


async def get(country):
    try:
        url = f"https://countryinfoapi.com/api/countries/name/{country}"
        country_file = "assets/data/countries.json"

        def load_data():
            with open(country_file, "r", encoding="utf-8") as file:
                data = json.load(file)
            return data

        def get_data(country_name):
            data = load_data()
            for country in data:
                if country["country"].lower() == country_name.lower():
                    famous_for = country.get("famous_for", "Unknown")
                    neighbors = country.get("neighbors", "Unknown")
                    return famous_for, neighbors
            return "None"

        famous_for, neighbors = get_data(country)

        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        name = data.get("name", "Unknown")
        capital = data.get("capital", ["Unknown"])[0]
        currency = (
            data.get("currencies", {})
            .get(list(data.get("currencies", {}).keys())[0], {})
            .get("name", "Unknown")
        )
        languages = ", ".join(data.get("languages", {}).values())
        callingcode = data.get("callingcode", "Unknown")
        driving_side = data.get("car", {}).get("side", "Unknown")
        area = "{:,} km²".format(data.get("area", 0))
        continents = ", ".join(data.get("continents", "Unknown"))
        tld = data.get("tld", "Unknown")[0]
        landlocked = "Yes" if data.get("landlocked") else "No"
        famousFor = ", ".join([item.capitalize() for item in famous_for.split(", ")])
        neighbors_split = ", ".join(neighbors)

        shortcode = data.get("cca2", "").lower()
        image_url = f"https://flagpedia.net/data/flags/h80/{shortcode}.png"

        data = {
            "name": name.lower(),
            "capital": capital.lower(),
            "currency": currency,
            "languages": languages.lower(),
            "phoneCode": callingcode,
            "famousFor": famousFor.lower(),
            "driveDirection": driving_side,
            "area": area,
            "continent": continents,
            "tld": tld,
            "landlocked": landlocked,
            "neighbours": neighbors_split,
            "flag": image_url,
        }

        return data

    except requests.RequestException as e:
        print(f"Error getting country info: {e}")
        return None
