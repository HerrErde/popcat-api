from io import BytesIO

import requests
from PIL import Image, ImageOps


def create(image_url):
    try:
        response = requests.get(image_url)
        response.raise_for_status()
        input_image = Image.open(BytesIO(response.content))

        if input_image.mode == "RGBA":
            input_image = input_image.convert("RGB")

        inverted_image = ImageOps.invert(input_image)

        output_bytes = BytesIO()
        inverted_image.save(output_bytes, format="PNG")

        return output_bytes.getvalue()

    except Exception as e:
        print(f"Error processing image: {e}")
        return None
