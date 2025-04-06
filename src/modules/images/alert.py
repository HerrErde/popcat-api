from io import BytesIO

from PIL import Image, ImageDraw, ImageFont

bg_image_path = "assets/img/images/alert.png"
text_position = (61, 825)
# TODO find right font
font_path = "assets/font/khula-regular.otf"


def create(text):
    try:
        bg_image = Image.open(bg_image_path).convert("RGBA")

        draw = ImageDraw.Draw(bg_image)
        custom_font = ImageFont.truetype(font_path, size=34)

        text_color = (0, 0, 0)
        draw.text(text_position, text, fill=text_color, font=custom_font)

        output_bytes = BytesIO()
        bg_image.save(output_bytes, format="PNG")
        return output_bytes.getvalue()

    except Exception as e:
        print(f"Error creating image: {e}")
        return None
