from io import BytesIO

from PIL import Image, ImageDraw, ImageFont

bg_image_path = "assets/img/images/facts.png"
font_path = "assets/font/Ascender-Sans-W01-Regular.ttf"
text_position = (-14, 330)
max_text_width = 100
max_text_height = 120
rotation_angle = -15
size = 32


def textsize(text, font):
    im = Image.new(mode="RGBA", size=(1, 1))
    draw = ImageDraw.Draw(im)
    width, height = draw.textbbox((0, 0), text=text, font=font)[2:]
    return width, height


def wrap_text(text, font, max_width, max_height):
    """Wrap text to fit within a maximum width and height."""
    lines = []
    words = text.split()
    if not words:
        return lines

    current_line = words[0]
    line_height = textsize(current_line, font)[1]

    for word in words[1:]:
        test_line = current_line + " " + word
        width, height = textsize(test_line, font)
        if width <= max_width and height <= max_height:
            current_line = test_line
        else:
            # Check if adding the current line would exceed max height
            if len(lines) * line_height + height > max_height:
                # If so, break the loop to prevent overflow
                break
            lines.append(current_line)
            current_line = word

    # Add the last line
    if current_line:
        lines.append(current_line)

    return lines


def create_text_layer(text, font, text_color, max_width, max_height, rotation_angle):
    """Create a high-resolution transparent layer with rotated text."""
    lines = wrap_text(text, font, max_width, max_height)

    # Create a high-resolution temporary image to calculate size
    temp_img = Image.new("RGBA", (1, 1), (255, 255, 255, 0))
    ImageDraw.Draw(temp_img)
    text_width = 0
    text_height = 0

    # Calculate the total width and height required
    for line in lines:
        w, h = textsize(line, font)
        text_width = max(text_width, w)
        text_height += h

    # Increase the size for better quality
    text_width *= 2
    text_height *= 2

    # Create the high-resolution transparent image for the text layer
    text_layer = Image.new("RGBA", (text_width, text_height), (255, 255, 255, 0))
    draw = ImageDraw.Draw(text_layer)

    # Draw the text on the transparent layer with higher resolution
    y = 0
    for line in lines:
        scaled_font = ImageFont.truetype(font_path, size)  # Scale font size
        draw.text((0, y), line, font=scaled_font, fill=text_color)
        y += textsize(line, scaled_font)[1]

    # Rotate the text layer
    rotated_layer = text_layer.rotate(
        rotation_angle, expand=1, resample=Image.BICUBIC, fillcolor=(255, 255, 255, 0)
    )

    return rotated_layer


def create(text):
    try:
        bg_image = Image.open(bg_image_path)
        bg_image = bg_image.convert("RGBA")

        custom_font = ImageFont.truetype(font_path, size)

        text_color = (0, 0, 0, 255)

        # Create a high-resolution transparent layer with rotated text
        rotated_text_layer = create_text_layer(
            text,
            custom_font,
            text_color,
            max_text_width,
            max_text_height,
            rotation_angle,
        )

        # Paste the rotated text layer onto the background image
        bg_image.paste(rotated_text_layer, text_position, rotated_text_layer)

        output_bytes = BytesIO()
        bg_image.save(output_bytes, format="PNG")

        return output_bytes.getvalue()

    except Exception as e:
        print(f"Error creating image: {e}")
        return None
