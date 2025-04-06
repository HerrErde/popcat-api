import math
import os
from io import BytesIO

import requests
from PIL import Image

folder_path = "pet"

resolutionsize = 128
size = 80
spriteposition = [30, 30]
squishiness = 0


def load_frame_images():
    frame_images = []
    max_frame_number = -1

    # Iterate over all files in the folder
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)

        # Check if the file is a directory (to handle nested folders)
        if os.path.isdir(file_path):
            # Recursively load frame images from subdirectory
            frame_images.extend(load_frame_images(file_path))
        elif filename.startswith("pet") and filename.endswith(".gif"):
            try:
                # Extract frame number from filename
                frame_number = int(filename.split("pet")[1].split(".")[0])
                if frame_number > max_frame_number:
                    max_frame_number = frame_number

                # Load frame image and append to list
                frame_image = Image.open(file_path).convert("RGBA")
                frame_images.append(frame_image)
            except ValueError:
                continue

    return frame_images


def makegifframe(
    number, patframes, sprite, spriteposition, size, squishiness, resolutionsize
):
    gif_frame = Image.new(
        "RGBA", (128 * (resolutionsize // 100), 128 * (resolutionsize // 100))
    )

    if sprite is not None:
        sine = math.sin((number + 1) * 5) * (12 + squishiness)
        s = size - sine if size - sine > 0 else 0
        s2 = size + sine if size + sine > 0 else 0
        render_sprite = sprite.resize(
            (int(s2 * (resolutionsize / 100)), int(s * (resolutionsize / 100)))
        )
        y = spriteposition[1] + (size - render_sprite.height)
        x = spriteposition[0] - (((render_sprite.width * 1) - size) / 2)
        gif_frame.paste(
            render_sprite,
            (int(x * (resolutionsize / 100)), int(y * (resolutionsize / 100))),
            render_sprite,
        )

    if 0 <= number < len(patframes):
        gif_frame.paste(
            patframes[number].resize(
                (128 * (resolutionsize // 100), 128 * (resolutionsize // 100))
            ),
            (
                0,
                int(
                    (math.sin((number + 1) * 5) * squishiness) * (resolutionsize // 100)
                ),
            ),
            patframes[number],
        )

    return gif_frame


def create(image_url):
    try:
        patframes = load_frame_images()

        sprite_response = requests.get(image_url)
        if sprite_response.status_code != 200:
            raise ValueError("Failed to retrieve the sprite image from URL.")
        sprite = Image.open(BytesIO(sprite_response.content)).convert("RGBA")

        images = []
        for v in range(len(patframes)):
            gif_frame = makegifframe(
                v, patframes, sprite, spriteposition, size, squishiness, resolutionsize
            )
            images.append(gif_frame)

        if not images:
            return None

        frame_duration = 33

        output_bytes = BytesIO()
        images[0].save(
            output_bytes,
            format="GIF",
            append_images=images[1:],
            save_all=True,
            duration=frame_duration,
            loop=0,
            disposal=2,
        )

        return output_bytes.getvalue()

    except Exception as e:
        print(f"Error creating image: {e}")
        return None


create("https://cdn.popcat.xyz/avatar.png")
