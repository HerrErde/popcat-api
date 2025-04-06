import re

import yaml


def morse_code(text):
    morse_code_dict = {
        "A": ".-",
        "B": "-...",
        "C": "-.-.",
        "D": "-..",
        "E": ".",
        "F": "..-.",
        "G": "--.",
        "H": "....",
        "I": "..",
        "J": ".---",
        "K": "-.-",
        "L": ".-..",
        "M": "--",
        "N": "-.",
        "O": "---",
        "P": ".--.",
        "Q": "--.-",
        "R": ".-.",
        "S": "...",
        "T": "-",
        "U": "..-",
        "V": "...-",
        "W": ".--",
        "X": "-..-",
        "Y": "-.--",
        "Z": "--..",
        "0": "-----",
        "1": ".----",
        "2": "..---",
        "3": "...--",
        "4": "....-",
        "5": ".....",
        "6": "-....",
        "7": "--...",
        "8": "---..",
        "9": "----.",
        " ": "/",
    }
    morse_code_message = []
    for char in text.upper():
        if char in morse_code_dict:
            morse_code_message.append(morse_code_dict[char])
        else:
            morse_code_message.append(
                ""
            )  # Leave a space for characters not in the dictionary

    return " ".join(morse_code_message)


def doublestruck_text(text):
    doublestruck_map = {
        "0": "𝟘",
        "1": "𝟙",
        "2": "𝟚",
        "3": "𝟛",
        "4": "𝟜",
        "5": "𝟝",
        "6": "𝟞",
        "7": "𝟟",
        "8": "𝟠",
        "9": "𝟡",
        "A": "𝔸",
        "B": "𝔹",
        "C": "ℂ",
        "D": "𝔻",
        "E": "𝔼",
        "F": "𝔽",
        "G": "𝔾",
        "H": "ℍ",
        "I": "𝕀",
        "J": "𝕁",
        "K": "𝕂",
        "L": "𝕃",
        "M": "𝕄",
        "N": "ℕ",
        "O": "𝕆",
        "P": "ℙ",
        "Q": "ℚ",
        "R": "ℝ",
        "S": "𝕊",
        "T": "𝕋",
        "U": "𝕌",
        "V": "𝕍",
        "W": "𝕎",
        "X": "𝕏",
        "Y": "𝕐",
        "Z": "ℤ",
        "a": "𝕒",
        "b": "𝕓",
        "c": "𝕔",
        "d": "𝕕",
        "e": "𝕖",
        "f": "𝕗",
        "g": "𝕘",
        "h": "𝕙",
        "i": "𝕚",
        "j": "𝕛",
        "k": "𝕜",
        "l": "𝕝",
        "m": "𝕞",
        "n": "𝕟",
        "o": "𝕠",
        "p": "𝕡",
        "q": "𝕢",
        "r": "𝕣",
        "s": "𝕤",
        "t": "𝕥",
        "u": "𝕦",
        "v": "𝕧",
        "w": "𝕨",
        "x": "𝕩",
        "y": "𝕪",
        "z": "𝕫",
    }

    doublestruck_text = "".join(doublestruck_map.get(char, char) for char in text)

    return doublestruck_text


dictionary_file = "assets/data/tranzlator.yml"


def translate(phrase):
    def load_dictionary(yaml_file):
        with open(yaml_file, "r", encoding="utf-8") as file:
            dictionary = yaml.safe_load(file)
        return dictionary

    def translate_line(line, dictionary):
        words = re.split(r"[ ,.!\n]+", line)
        translated_words = [dictionary.get(word, word) for word in words]
        return " ".join(translated_words)

    dictionary = load_dictionary(dictionary_file)
    lines = phrase.split("\n")
    translated_lines = [translate_line(line, dictionary) for line in lines]

    return "\n".join(translated_lines).strip()
