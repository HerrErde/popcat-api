from io import BytesIO

from PIL import Image, ImageDraw, ImageFont

bg_image_path = "assets/img/images/pikachu.png"
text_position = (220, 42)
font_path = "assets/font/segoe_ui.ttf"
max_width = 410
max_height = 160
font_size = 33


def textsize(text, font):
    im = Image.new(mode="RGBA", size=(1, 1))
    draw = ImageDraw.Draw(im)
    width, height = draw.textbbox((0, 0), text=text, font=font)[2:]
    return width, height


def wrap_text(text, font, max_width):
    """Wrap text to fit within a maximum width."""
    lines = []
    words = text.split()
    if not words:
        return lines

    current_line = words[0]
    for word in words[1:]:
        test_line = current_line + " " + word
        width, _ = textsize(test_line, font)
        if width <= max_width:
            current_line = test_line
        else:
            lines.append(current_line)
            current_line = word
    lines.append(current_line)

    return lines


def draw_wrapped_text(draw, text, position, font, text_color, max_width, max_height):
    lines = wrap_text(text, font, max_width)

    # Get total height required for all lines
    total_text_height = (
        sum(textsize(line, font)[1] for line in lines) + (len(lines) - 1) * 5
    )  # Line spacing

    # Limit height if necessary
    y_center = position[1]
    if total_text_height > max_height:
        total_text_height = max_height

    # Calculate vertical centering within max_height
    y_start = y_center - total_text_height / 2
    y = y_start

    drawn_lines = []
    current_height = 0

    # Determine which lines fit within max_height
    for line in lines:
        text_width, text_height = textsize(line, font)
        if current_height + text_height > max_height:
            break
        drawn_lines.append(line)
        current_height += text_height + 5  # Account for line spacing

    # Draw the text lines
    for line in drawn_lines:
        text_width, text_height = textsize(line, font)
        draw.text((position[0] - text_width / 2, y), line, font=font, fill=text_color)
        y += text_height + 5  # Move to the next line


def create(text):
    try:

        bg_image = Image.open(bg_image_path)
        bg_image = bg_image.convert("RGBA")

        draw = ImageDraw.Draw(bg_image)

        font = ImageFont.truetype(font_path, size=font_size)

        text_color = (0, 0, 0)  # Black color (RGB)

        draw_wrapped_text(
            draw, text, text_position, font, text_color, max_width, max_height
        )

        output_bytes = BytesIO()
        bg_image.save(output_bytes, format="PNG")

        return output_bytes.getvalue()

    except Exception as e:
        print(f"Error creating image: {e}")
        return None
