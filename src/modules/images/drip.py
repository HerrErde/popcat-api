from io import BytesIO

import requests
from PIL import Image

bg_image_path = "assets/img/images/drip.png"

crop_region = (330, 135, 555, 360)
width = crop_region[2] - crop_region[0]
height = crop_region[3] - crop_region[1]


def create(image_url):
    try:
        response = requests.get(image_url)
        response.raise_for_status()
        input_image = (
            Image.open(BytesIO(response.content))
            .convert("RGBA")
            .resize((width, height))
        )

        bg_image = Image.open(bg_image_path).convert("RGBA")

        output_image = Image.new("RGBA", bg_image.size)

        output_image.paste(image, crop_region)

        output_image.paste(bg_image, (0, 0), bg_image)

        output_bytes = BytesIO()
        output_image.save(output_bytes, format="PNG")

        return output_bytes.getvalue()

    except Exception as e:
        print(f"Error creating image: {e}")
        return None
