from io import BytesIO

import requests
from PIL import Image


def create(image_url, deg):
    try:
        response = requests.get(image_url)
        response.raise_for_status()
        input_image = Image.open(BytesIO(response.content))

        input_hsv_image = input_image.convert("HSV")

        # Separate the HSV components
        h, s, v = input_hsv_image.split()

        # Adjust hue by rotating it
        hue_shift = (
            float(deg) / 360.0
        )  # Convert degrees to fraction of a full rotation (360 degrees)
        h_data = h.load()
        width, height = h.size

        for y in range(height):
            for x in range(width):
                current_hue = h_data[x, y] / 255.0  # Normalize hue value (0-1)
                new_hue = (current_hue + hue_shift) % 1.0  # Apply hue shift
                # Scale hue back to 0-255 range
                h_data[x, y] = int(new_hue * 255.0)

        # Merge back the modified HSV components
        adjusted_hsv_image = Image.merge("HSV", (h, s, v))

        # Convert HSV image back to RGB
        adjusted_rgb_image = adjusted_hsv_image.convert("RGB")

        output_bytes = BytesIO()
        adjusted_rgb_image.save(output_bytes, format="PNG")

        return output_bytes.getvalue()

    except Exception as e:
        print(f"Error processing image: {e}")
        return None
