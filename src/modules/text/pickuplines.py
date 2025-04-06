import json
import random

file_path = "assets/data/pickuplines.json"


def text():
    with open(file_path, "r") as file:
        data = json.load(file)

    if data:
        text = random.choice(data)
        return text
    else:
        print("No data loaded from JSON file!")
        return None
