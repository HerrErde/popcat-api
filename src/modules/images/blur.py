from io import BytesIO

import requests
from PIL import Image, ImageFilter

blur_factor = 4


def create(image_url):
    try:
        response = requests.get(image_url)
        response.raise_for_status()
        input_image = Image.open(BytesIO(response.content))

        blurred_image = input_image.filter(ImageFilter.GaussianBlur(blur_factor))

        output_bytes = BytesIO()
        blurred_image.save(output_bytes, format="PNG")

        return output_bytes.getvalue()

    except Exception as e:
        print(f"Error processing image: {e}")
        return None
