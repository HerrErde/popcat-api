from io import BytesIO

import requests
from PIL import Image

image_path = "uncover.png"
image_path2 = "uncover2.png"

crop_region = (63, 581, 219, 739)
crop_region2 = (61, 675)
output_width = crop_region[2] - crop_region[0]
output_height = crop_region[3] - crop_region[1]


def create(image_url):
    try:
        response = requests.get(image_url)
        response.raise_for_status()

        fetched_image = Image.open(BytesIO(response.content)).convert("RGBA")
        fetched_image = fetched_image.resize((output_width, output_height))

        bg_image = Image.open(image_path).convert("RGBA")
        bg_image2 = Image.open(image_path2).convert("RGBA")

        output_image = Image.new("RGBA", bg_image.size)

        output_image.paste(bg_image, (0, 0), bg_image)

        output_image.paste(fetched_image, crop_region, fetched_image)

        output_image.paste(bg_image2, crop_region2, bg_image2)

        output_bytes = BytesIO()
        output_image.save(output_bytes, format="PNG")

        return output_bytes.getvalue()

    except requests.exceptions.RequestException as e:
        print(f"Error fetching the image: {e}")
        return None

    except IOError as e:
        print(f"Error processing images: {e}")
        return None

    except Exception as e:
        print(f"Unexpected error: {e}")
        return None
