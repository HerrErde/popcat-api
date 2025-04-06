import random

import requests

from config import config


def text():
    urls = [
        "https://api.api-ninjas.com/v1/facts",
        "https://uselessfacts.jsph.pl/api/v2/facts/random",
        "https://useless.dotenv.dev/api/random",
    ]

    url = random.choice(urls)

    headers = {"Accept": "application/json"}
    if config.api_ninjas_key and url == "https://api.api-ninjas.com/v1/facts":
        headers["X-Api-Key"] = config.api_ninjas_key

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()

        if url == "https://api.api-ninjas.com/v1/facts":
            fact = data[0].get("fact")
        elif url == "https://uselessfacts.jsph.pl/api/v2/facts/random":
            fact = data.get("text")
        elif url == "https://useless.dotenv.dev/api/random":
            fact = data.get("fact")
        else:
            fact = "No fact available."

        return fact

    except requests.exceptions.RequestException as e:
        print(f"Error fetching joke: {e}")
        return "Error fetching joke."
