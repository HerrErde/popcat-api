from io import BytesIO

import requests
from PIL import Image

bg_image_path = "assets/img/images/jail.png"
width = 500
height = 500


def create(image_url):
    try:
        response = requests.get(image_url)
        response.raise_for_status()
        input_image = (
            Image.open(BytesIO(response.content))
            .convert("RGBA")
            .resize((width, height))
        )

        bg_image = Image.open(bg_image_path).convert("RGBA").resize((width, height))

        output_image = Image.alpha_composite(input_image, bg_image)

        output_bytes = BytesIO()
        output_image.save(output_bytes, format="PNG")

        return output_bytes.getvalue()

    except Exception as e:
        print(f"Error overlaying image: {e}")
        return None
