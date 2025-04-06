from io import BytesIO

from PIL import Image, ImageDraw, ImageFont

bg_image_path = "assets/img/images/pooh.png"
text1_position = (570, 145)
text2_position = (570, 438)
font_path = "assets/font/PrimaSansBT-Roman.otf"
text_color = (0, 0, 0)
max_text_width = 450
max_text_height = 500
font_size = 50
line_spacing = 2


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


def calculate_optimal_font_size(text, max_width, max_height, font_size):
    while font_size > 10:  # Avoid going too small
        font = ImageFont.truetype(font_path, size=font_size)
        lines = wrap_text(text, font, max_width)
        total_text_height = (
            sum(textsize(line, font)[1] for line in lines)
            + (len(lines) - 1) * line_spacing
        )

        if total_text_height <= max_height:
            return font_size
        font_size -= 1

    return font_size


def draw_wrapped_text(draw, text, position, font, text_color, max_width, line_spacing):
    lines = wrap_text(text, font, max_width)
    total_text_height = (
        sum(textsize(line, font)[1] for line in lines) + (len(lines) - 1) * line_spacing
    )

    x = position[0] - max_text_width / 2  # Center horizontally
    y = position[1] - total_text_height / 2  # Center vertically

    for line in lines:
        text_width, text_height = textsize(line, font)
        draw.text(
            (x + (max_text_width - text_width) / 2, y), line, font=font, fill=text_color
        )
        y += text_height + line_spacing


def create(text1, text2):
    try:
        bg_image = Image.open(bg_image_path).convert("RGBA")
        draw = ImageDraw.Draw(bg_image)

        # Handle text1
        font_size1 = calculate_optimal_font_size(
            text1, max_text_width, max_text_height, font_size
        )
        font1 = ImageFont.truetype(font_path, size=font_size1)
        draw_wrapped_text(
            draw, text1, text1_position, font1, text_color, max_text_width, line_spacing
        )

        # Handle text2
        font_size2 = calculate_optimal_font_size(
            text2, max_text_width, max_text_height, font_size
        )
        font2 = ImageFont.truetype(font_path, size=font_size2)
        draw_wrapped_text(
            draw, text2, text2_position, font2, text_color, max_text_width, line_spacing
        )

        output_bytes = BytesIO()
        bg_image.save(output_bytes, format="PNG")

        return output_bytes.getvalue()

    except Exception as e:
        print(f"Error creating image: {e}")
        return None
