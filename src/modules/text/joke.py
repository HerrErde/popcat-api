import random

import requests

from config import config


def text():
    urls = [
        "https://api.api-ninjas.com/v1/jokes",
        "https://icanhazdadjoke.com/",
        "https://official-joke-api.appspot.com/jokes/random",
        "https://v2.jokeapi.dev/joke/Any",
    ]

    url = random.choice(urls)

    headers = {"Accept": "application/json"}
    if config.api_ninjas_key and url == "https://api.api-ninjas.com/v1/jokes":
        headers["X-Api-Key"] = config.api_ninjas_key

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()

        if url == "https://api.api-ninjas.com/v1/jokes":
            joke = data[0].get("joke")
        elif url == "https://v2.jokeapi.dev/joke/Any":
            setup = data.get("setup")
            delivery = data.get("delivery")
            joke = f"{setup} {delivery}" if setup and delivery else data.get("joke")
        elif url == "https://official-joke-api.appspot.com/jokes/random":
            setup = data.get("setup")
            punchline = data.get("punchline")
            joke = f"{setup} {punchline}"
        elif url == "https://icanhazdadjoke.com/":
            joke = data.get("joke")
        else:
            joke = "No joke available."

        return joke

    except requests.exceptions.RequestException as e:
        print(f"Error fetching joke: {e}")
        return "Error fetching joke."
