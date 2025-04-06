from io import BytesIO

import requests
from PIL import Image, ImageOps


def create(image_url):
    try:
        response = requests.get(image_url)
        response.raise_for_status()

        input_image = Image.open(BytesIO(response.content))

        grayscale_image = ImageOps.grayscale(input_image)

        output_bytes = BytesIO()
        grayscale_image.save(output_bytes, format="PNG")

        return output_bytes.getvalue()

    except Exception as e:
        print(f"Error processing image: {e}")
        return None
