import json
import random
from io import BytesIO

from PIL import Image

ntc_path = "assets/data/ntc.json"


def hex_to_rgb(hex_color):
    return tuple(int(hex_color[i : i + 2], 16) for i in (0, 2, 4))


def rgb_to_str(rgb_values):
    return f"rgb({rgb_values[0]},{rgb_values[1]},{rgb_values[2]})"


def lighten_color(hex_color, amount=50):
    r, g, b = hex_to_rgb(hex_color)
    factor = amount / 100.0

    r = min(255, int(r + (255 - r) * factor))
    g = min(255, int(g + (255 - g) * factor))
    b = min(255, int(b + (255 - b) * factor))

    return f"{r:02x}{g:02x}{b:02x}"


def get_color_name(hex_color):
    hex_color = hex_color.upper()
    with open(ntc_path, "r") as file:
        color_data = json.load(file)
        for color_entry in color_data:
            if hex_color in color_entry:
                return color_entry[hex_color]
    return "Black"


def randomcolor(domain):
    red = random.randint(0, 255)
    green = random.randint(0, 255)
    blue = random.randint(0, 255)

    # Convert the RGB values to a hex color string
    hex_color = "{:02x}{:02x}{:02x}".format(red, green, blue).upper()

    get_color_name(hex_color)

    f"{domain}/color/image/{hex_color}"

    return {
        "hex": hex_color,
        "name": get_color_name(hex_color),
        "image": f"{domain}/color/image/{hex_color}",
    }


def color_info(hex_color, domain):
    rgb_values = hex_to_rgb(hex_color)
    brightened = lighten_color(hex_color, 50)

    return {
        "hex": f"#{hex_color}",
        "name": get_color_name(hex_color),
        "rgb": rgb_to_str(rgb_values),
        "color_image": f"{domain}/color/image/{hex_color}",
        "brightened": f"#{brightened}",
    }


def create(hex_color):
    try:
        size = (500, 500)

        image = Image.new("RGB", size, hex_to_rgb(hex_color))

        output_bytes = BytesIO()
        image.save(output_bytes, format="PNG")

        return output_bytes.getvalue()

    except Exception as e:
        print(f"Error creating image: {e}")
        return None
