import random


def mock(text):
    mocked_text = ""
    for char in text:
        if random.choice([True, False]):
            mocked_text += char.upper()
        else:
            mocked_text += char.lower()

    return mocked_text
