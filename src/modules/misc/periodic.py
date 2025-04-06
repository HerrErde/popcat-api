import json
import random
from io import BytesIO

from PIL import Image, ImageDraw, ImageFont

periodic_file_path = "assets/data/PeriodicTableJSON.json"

font_path = "assets/font/Eina01-Bold.ttf"
font_path2 = "assets/font/NeverMind-Bold.ttf"
font_path3 = "assets/font/NeverMind-Regular.ttf"


def load_periodic_table():
    with open(periodic_file_path, "r", encoding="utf-8") as file:
        data = json.load(file)
    return data


def get_element(element, domain):
    elements = load_periodic_table()["elements"]

    # Lookup by name, symbol, or atomic number
    for el in elements:
        if (
            el["name"].lower() == element.lower()
            or el["symbol"].lower() == element.lower()
            or str(el["number"]) == element
        ):
            return {
                "name": el["name"],
                "symbol": el["symbol"],
                "atomic_number": el["number"],
                "atomic_mass": el.get("atomic_mass", "Unknown"),
                "period": el.get("period", "Unknown"),
                "phase": el.get("phase", "Unknown"),
                "discovered_by": el.get("discovered_by", "Unknown"),
                "image": f"{domain}/periodic-table/image/{el['number']}",
                "summary": el.get("summary", "No summary available."),
            }

    # If no element is found
    return None


def get_random_element():
    elements = load_periodic_table()["elements"]
    random_element = random.choice(elements)

    return (
        random_element["name"],
        random_element["symbol"],
        random_element["number"],
        random_element["atomic_mass"],
        random_element["period"],
        random_element["phase"],
        random_element["discovered_by"],
        random_element["summary"],
    )


def create(element):
    width, height = 500, 500
    text_color = (242, 194, 1)  # RGB value for #f2c201
    bg_color = (53, 64, 77)  # RGB value for #35404d

    def textsize(text, font):
        im = Image.new(mode="RGB", size=(1, 1))
        draw = ImageDraw.Draw(im)
        width, height = draw.textbbox((0, 0), text=text, font=font)[
            2:
        ]  # Get width and height
        return width, height

    def draw_square(draw):
        # Function to draw a colored square (rectangle) on the image
        square_color = text_color
        # (x0, y0, x1, y1) for the rectangle
        square_coords = (0, 470, 499, 499)
        draw.rectangle(square_coords, fill=square_color)

    def draw_info(draw):
        # Define text positions and font sizes
        text_pos1 = (250, 58)  # Centered horizontally
        text_pos2 = (250, 112)  # Centered horizontally
        text_pos3 = (250, 372)  # Centered horizontally
        text_pos4 = (250, 412)  # Centered horizontally

        font1 = ImageFont.truetype(font_path2, size=45)
        font2 = ImageFont.truetype(font_path3, size=220)
        font3 = ImageFont.truetype(font_path2, size=30)
        font4 = ImageFont.truetype(font_path, size=48)

        elements = load_periodic_table()["elements"]

        # Lookup the element information
        found_element = None
        for el in elements:
            if str(el["number"]) == element or el["symbol"] == element.upper():
                found_element = el
                break

        if found_element:
            # Draw element information on the image
            atomic_number = found_element["number"]
            symbol = found_element["symbol"]
            atomic_mass = found_element["atomic_mass"]
            name = found_element["name"]

            # Calculate centered positions
            text_width1, _ = textsize(f"{atomic_number}", font=font1)
            text_width2, _ = textsize(symbol, font=font2)
            text_width3, _ = textsize(f"{atomic_mass}", font=font3)
            text_width4, _ = textsize(name, font=font4)

            # Update text positions to center horizontally
            text_pos1 = (250 - text_width1 // 2, text_pos1[1])
            text_pos2 = (250 - text_width2 // 2, text_pos2[1])
            text_pos3 = (250 - text_width3 // 2, text_pos3[1])
            text_pos4 = (250 - text_width4 // 2, text_pos4[1])

            draw.text(text_pos1, f"{atomic_number}", fill=text_color, font=font1)
            draw.text(text_pos2, symbol, fill=text_color, font=font2)
            draw.text(text_pos3, f"{atomic_mass}", fill=text_color, font=font3)
            draw.text(text_pos4, name, fill=text_color, font=font4)

    try:
        # Create a new image with the specified size and color
        image = Image.new("RGB", (width, height), bg_color)

        # Draw on the image using ImageDraw
        draw = ImageDraw.Draw(image)

        draw_square(draw)
        draw_info(draw)

        output_bytes = BytesIO()
        image.save(output_bytes, format="PNG")

        return output_bytes.getvalue()

    except Exception as e:
        print(f"Error creating image: {e}")
        return None
