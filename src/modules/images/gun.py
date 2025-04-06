from io import BytesIO

import requests
from PIL import Image, ImageDraw, ImageFont

image_path = "assets/img/images/gun.png"
font_path = "assets/font/NimbusSanL-Reg.otf"


def create(image_url, text=None):
    try:
        response = requests.get(image_url)
        response.raise_for_status()
        bg_image = Image.open(BytesIO(response.content)).convert("RGBA")

        overlay = Image.open(image_path).convert("RGBA")

        bg_image = bg_image.resize(overlay.size)

        output = Image.alpha_composite(bg_image, overlay)

        if text:
            text_overlay = Image.new("RGBA", output.size, (255, 255, 255, 0))
            draw = ImageDraw.Draw(text_overlay)

            font = ImageFont.truetype(font_path, 40)
            text_width, text_height = draw.textbbox((0, 0), text, font=font)[2:]

            # Positioning
            text_y = output.height - 230

            rect_x1 = 0
            rect_y1 = text_y - 18
            rect_x2 = output.width
            rect_y2 = text_y + text_height + 17

            text_x = (output.width - text_width) // 2

            # Draw full-width semi-transparent rectangle
            draw.rectangle([rect_x1, rect_y1, rect_x2, rect_y2], fill=(0, 0, 0, 130))
            draw.text((text_x, text_y), text, font=font, fill="white")

            output = Image.alpha_composite(output, text_overlay)

        buffer = BytesIO()
        output.save(buffer, format="PNG")
        return buffer.getvalue()

    except Exception as e:
        print(f"Error creating image: {e}")
        return None
