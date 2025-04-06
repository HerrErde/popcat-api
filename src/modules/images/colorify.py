import imghdr
from io import BytesIO

import numpy as np
import requests
from PIL import Image


def is_valid_image(image_bytes):
    image_format = imghdr.what(None, h=image_bytes)
    return image_format is not None


def hex_to_rgb(hex_color):
    return tuple(int(hex_color[i : i + 2], 16) for i in (0, 2, 4))


def rgb_to_hsl(r, g, b):
    r, g, b = r / 255.0, g / 255.0, b / 255.0
    max_val = max(r, g, b)
    min_val = min(r, g, b)
    delta = max_val - min_val

    # Calculate lightness
    lightness = (max_val + min_val) / 2.0

    if delta == 0:  # Grayscale
        hue = 0.0
        saturation = 0.0
    else:
        # Calculate saturation
        saturation = delta / (1 - abs(2 * lightness - 1))

        # Calculate hue
        if max_val == r:
            hue = (g - b) / delta + (6 if g < b else 0)
        elif max_val == g:
            hue = (b - r) / delta + 2
        else:
            hue = (r - g) / delta + 4
        hue = (hue * 60) % 360

    return hue, saturation, lightness


def apply_tint(image, tint_color):
    img_array = np.array(image)
    rgb = img_array[:, :, :3].astype(np.float32)
    alpha = img_array[:, :, 3]

    # Convert tint color to HSL
    tint_r, tint_g, tint_b = hex_to_rgb(tint_color)
    hue_tint, saturation_tint, _ = rgb_to_hsl(tint_r, tint_g, tint_b)
    hue_tint = hue_tint % 360  # Ensure hue is within [0, 360)

    # Compute lightness for each pixel
    rgb_norm = rgb / 255.0
    max_val = np.max(rgb_norm, axis=2)
    min_val = np.min(rgb_norm, axis=2)
    lightness = (max_val + min_val) / 2.0

    # Calculate c, x, m for HSL to RGB conversion
    c = (1 - np.abs(2 * lightness - 1)) * saturation_tint
    x = c * (1 - np.abs((hue_tint / 60) % 2 - 1))
    m = lightness - c / 2

    # Determine RGB prime based on hue interval
    if 0 <= hue_tint < 60:
        r_prime, g_prime, b_prime = c, x, np.zeros_like(c)
    elif 60 <= hue_tint < 120:
        r_prime, g_prime, b_prime = x, c, np.zeros_like(c)
    elif 120 <= hue_tint < 180:
        r_prime, g_prime, b_prime = np.zeros_like(c), c, x
    elif 180 <= hue_tint < 240:
        r_prime, g_prime, b_prime = np.zeros_like(c), x, c
    elif 240 <= hue_tint < 300:
        r_prime, g_prime, b_prime = x, np.zeros_like(c), c
    else:
        r_prime, g_prime, b_prime = c, np.zeros_like(c), x

    # Calculate new RGB values
    new_r = (r_prime + m) * 255.0
    new_g = (g_prime + m) * 255.0
    new_b = (b_prime + m) * 255.0

    # Combine and clip
    new_rgb = np.stack([new_r, new_g, new_b], axis=2)
    new_rgb = np.clip(new_rgb, 0, 255).astype(np.uint8)

    # Merge with alpha and create image
    tinted_array = np.dstack((new_rgb, alpha))
    return Image.fromarray(tinted_array, "RGBA")


def create(image_url, color):
    try:
        # Fetch the image
        response = requests.get(image_url)
        response.raise_for_status()
        image_bytes = response.content

        if not is_valid_image(image_bytes):
            return None, False

        # Open the image and apply the tint
        image = Image.open(BytesIO(image_bytes)).convert("RGBA")
        tinted_image = apply_tint(image, color)

        output_bytes = BytesIO()
        tinted_image.save(output_bytes, format="PNG")
        return output_bytes.getvalue(), True

    except Exception as e:
        print(f"Error recoloring image: {e}")
        return None, False


"""

const { createCanvas, loadImage } = require('canvas');
const fs = require('fs');

async function tintImage(inputImage, hexColor, outputImage) {
  try {
    // Load the input image
    const img = await loadImage(inputImage);

    // Create a canvas with the same dimensions as the image
    const canvas = createCanvas(img.width, img.height);
    const ctx = canvas.getContext('2d');

    // Draw the original image onto the canvas
    ctx.drawImage(img, 0, 0, canvas.width, canvas.height);

    // Apply the tint overlay the first time
    applyTint(ctx, hexColor, canvas);

    // Save the canvas content as an image
    const buffer = canvas.toBuffer('image/png');
    fs.writeFileSync(outputImage, buffer);

    console.log(`Image successfully saved to ${outputImage}`);
  } catch (error) {
    console.error(`Failed to process the image: ${error.message}`);
  }
}

function applyTint(ctx, hexColor, canvas) {
  // Apply the tint overlay
  ctx.fillStyle = hexColor; // Use the provided hex color for the tint
  ctx.globalCompositeOperation = 'color'; // Blend mode to retain image details
  ctx.fillRect(0, 0, canvas.width, canvas.height); // Fill the entire canvas with the color

  // Reset composite operation to default
  ctx.globalCompositeOperation = 'source-over';
}

// Example usage
const inputImage = 'avatar.png'; // Path to your input image
const outputImage = 'tint-avatar.png'; // Path to save the tinted image
const hexColor = '#7289da'; // Desired tint color

tintImage(inputImage, hexColor, outputImage);

"""
