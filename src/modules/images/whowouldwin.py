from io import BytesIO

import aiohttp
from PIL import Image

bg_image_path = "assets/img/images/whowouldwin.png"
region1 = (41, 124, 359, 449)
region2 = (461, 124, 779, 449)

width1 = region1[2] - region1[0]
height1 = region1[3] - region1[1]
width2 = region2[2] - region2[0]
height2 = region2[3] - region2[1]


async def create(image1, image2):
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(image1) as response1, session.get(
                image2
            ) as response2:
                response1.raise_for_status()
                response2.raise_for_status()

                image1 = Image.open(BytesIO(await response1.read())).convert("RGBA")
                image2 = Image.open(BytesIO(await response2.read())).convert("RGBA")

                bg_image = Image.open(bg_image_path).convert("RGBA")

                image1 = image1.resize((width1, height1))
                image2 = image2.resize((width2, height2))

                output_image = Image.new("RGBA", bg_image.size)
                output_image.paste(bg_image, (0, 0), bg_image)
                output_image.paste(image1, region1[:2], image1)
                output_image.paste(image2, region2[:2], image2)

                output_bytes = BytesIO()
                output_image.save(output_bytes, format="PNG")

                return output_bytes.getvalue()

    except Exception as e:
        print(f"Error creating image: {e}")
        return None
