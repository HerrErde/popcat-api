import json
import random

file_path = "assets/data/wyr_questions.json"


def text():
    with open(file_path, "r") as file:
        data = json.load(file)

    random_question = random.choice(data)

    ops1 = random_question["ops1"]
    ops2 = random_question["ops2"]

    return ops1, ops2
