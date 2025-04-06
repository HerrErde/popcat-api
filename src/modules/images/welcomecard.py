from io import BytesIO

import aiohttp
from PIL import Image, ImageDraw, ImageFont

font_path = "assets/font/tt_rounds_cprs_bold.ttf"
width, height = 1024, 500
border_width = 9

font_large = ImageFont.truetype(font_path, 75)
font_medium = ImageFont.truetype(font_path, 45)
font_small = ImageFont.truetype(font_path, 35)


def create_circular_mask(size):
    """Create a circular mask (L mode)"""
    mask = Image.new("L", size, 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((0, 0, size[0], size[1]), fill=255)
    return mask


def draw_colored_circle(base_img, center, radius, border_size, color):
    """Draw anti-aliased ring with transparent center and black outline"""
    x, y = center
    outer_radius = radius + border_size
    inner_radius = radius
    outline_width = 1  # px

    # Supersample scale
    scale = 4
    temp_size = (outer_radius * 2 + outline_width * 2) * scale
    temp_img = Image.new("RGBA", (temp_size, temp_size), (0, 0, 0, 0))
    temp_draw = ImageDraw.Draw(temp_img)

    cx, cy = temp_size // 2, temp_size // 2

    # Draw outer black outline
    temp_draw.ellipse(
        (
            cx - (outer_radius + outline_width) * scale,
            cy - (outer_radius + outline_width) * scale,
            cx + (outer_radius + outline_width) * scale,
            cy + (outer_radius + outline_width) * scale,
        ),
        fill=(0, 0, 0, 255),
    )

    # Draw colored ring
    temp_draw.ellipse(
        (
            cx - outer_radius * scale,
            cy - outer_radius * scale,
            cx + outer_radius * scale,
            cy + outer_radius * scale,
        ),
        fill=color,
    )

    # Punch out inner transparent hole
    temp_draw.ellipse(
        (
            cx - inner_radius * scale,
            cy - inner_radius * scale,
            cx + inner_radius * scale,
            cy + inner_radius * scale,
        ),
        fill=(0, 0, 0, 0),
    )

    # Downscale to normal size with anti-aliasing
    final_ring = temp_img.resize(
        ((outer_radius + outline_width) * 2, (outer_radius + outline_width) * 2),
        Image.Resampling.LANCZOS,
    )

    # Paste onto base image
    paste_pos = (x - outer_radius - outline_width, y - outer_radius - outline_width)
    base_img.alpha_composite(final_ring, paste_pos)


async def create(background_url, text1, text2, text3, avatar_url, hex_color):
    try:
        async with aiohttp.ClientSession() as session:
            # Load background image
            bg_img = (
                Image.open(BytesIO(await (await session.get(background_url)).read()))
                .resize((width, height), Image.Resampling.LANCZOS)
                .convert("RGBA")
            )

            # Load avatar
            avatar_img = Image.open(
                BytesIO(await (await session.get(avatar_url)).read())
            ).convert("RGBA")

            # Color conversion
            rgb = tuple(int(hex_color[i : i + 2], 16) for i in (0, 2, 4))
            circle_color = rgb + (255,)

            # Circle parameters
            center = (width // 2, height // 3)
            radius = 119

            # Draw ring around avatar
            draw_colored_circle(bg_img, center, radius, border_width, circle_color)

            # Resize and mask avatar with anti-aliasing
            avatar_size = (radius * 2, radius * 2)
            avatar_img = avatar_img.resize(
                avatar_size, Image.Resampling.LANCZOS
            ).convert("RGBA")

            # Create anti-aliased mask at 4x resolution
            mask_size = (avatar_size[0] * 4, avatar_size[1] * 4)
            mask = create_circular_mask(mask_size)
            mask = mask.resize(avatar_size, Image.Resampling.LANCZOS)

            # Apply mask
            avatar_img.putalpha(mask)

            # Composite avatar smoothly onto background
            avatar_pos = (center[0] - radius, center[1] - radius)
            bg_img.alpha_composite(avatar_img, avatar_pos)

            # Draw text
            draw = ImageDraw.Draw(bg_img)
            text_params = [
                (text1, font_large, 281),
                (text2, font_medium, 356),
                (text3, font_small, 416),
            ]

            for text, font, y in text_params:
                bbox = draw.textbbox((0, 0), text, font=font)
                w = bbox[2]
                draw.text((center[0] - w / 2, y), text, fill=circle_color, font=font)

            # Export image
            output_image = BytesIO()
            bg_img.save(output_image, "PNG", optimize=True)
            return output_image.getvalue()

    except Exception as e:
        print(f"Error: {str(e)}")
        return None
