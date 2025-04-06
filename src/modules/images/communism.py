from io import BytesIO

import requests
from PIL import Image

overlay_image_path = "assets/img/images/communism.png"
width = 1024
height = 1024
opacity = 0.4


def reduce_opacity(image, opacity):
    """Return an image with reduced opacity."""
    if image.mode != "RGBA":
        image = image.convert("RGBA")

    alpha = image.getchannel("A")
    alpha = alpha.point(lambda p: int(p * opacity))
    image.putalpha(alpha)
    return image


def create(image_url):
    try:
        response = requests.get(image_url)
        response.raise_for_status()

        input_image = (
            Image.open(BytesIO(response.content))
            .convert("RGBA")
            .resize((width, height))
        )

        # Open the predefined overlay image
        overlay = Image.open(overlay_image_path).convert("RGBA").resize((width, height))

        # Make the overlay image 50% transparent
        overlay = reduce_opacity(overlay, opacity)
        input_image.paste(
            Image.new("RGBA", input_image.size, (255, 255, 255, 160)),
            (0, 0),
            Image.new("RGBA", input_image.size, (255, 255, 255, 128)),
        )

        # Blend the images together using alpha compositing
        blended_image = Image.alpha_composite(input_image, overlay)

        output_bytes = BytesIO()
        blended_image.save(output_bytes, format="PNG")

        return output_bytes.getvalue()

    except Exception as e:
        print(f"Error overlaying image: {e}")
        return None
