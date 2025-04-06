from io import BytesIO

import requests
from petpetgif import petpet


def create(image_url):
    try:

        response = requests.get(image_url)
        response.raise_for_status()

        image_bytes = BytesIO(response.content)

        output_bytes = BytesIO()
        petpet.make(image_bytes, output_bytes)

        return output_bytes.getvalue()

    except Exception as e:
        print(f"Error creating image: {e}")
        return None
