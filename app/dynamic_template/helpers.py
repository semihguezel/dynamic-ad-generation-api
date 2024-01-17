import textwrap
from PIL import Image, ImageDraw, ImageFont


def resize_and_round_corners(image, target_size=(360, 360), corner_radius=20):
    """
    Resize the image and create a new image with rounded corners.

    Args:
        image (Pillow.Image): Input image.
        target_size (tuple): The target size of the image (default is (360, 360)).
        corner_radius (int): The radius of the rounded corners (default is 20).

    Returns:
        Pillow.Image: The resulting image with rounded corners.
    """
    # Resize the image to the target size
    resized_image = image.resize(target_size)

    # Create a new image with rounded corners
    rounded_image = Image.new("RGB", resized_image.size, "white")
    mask = Image.new("L", resized_image.size, 0)
    draw = ImageDraw.Draw(mask)
    draw.rounded_rectangle([(0, 0), resized_image.size], radius=corner_radius, fill=255)
    rounded_image.paste(resized_image, mask=mask)

    # Save the resulting image
    return rounded_image


def write_multiline_text(draw, text, position, font, font_color, margin, max_height):
    """
    Write multiline text on an image with a specified font, color, and maximum height.

    Args:
        draw (ImageDraw.Draw): The drawing context.
        text (str): The text to be written.
        position (tuple): The starting position of the text.
        font (ImageFont.FreeTypeFont): The font to be used.
        font_color (str): The color of the text.
        margin (int): The margin between lines.
        max_height (int): The maximum height allowed for the text.

    Returns:
        tuple: The final position and font size.
    """
    # Wrap text to fit within the specified width
    font_width = font.getbbox("A")[2] // 1.5
    wrapped_text = textwrap.fill(text, width=int(position[0] / font_width))

    # Draw the wrapped text
    lines = wrapped_text.split("\n")
    total_text_height = sum(font.getbbox(line)[3] - font.getbbox(line)[1] for line in lines)
    safe_margin_y = position[1] + total_text_height

    if safe_margin_y + total_text_height > max_height:
        while True:
            if position[1] < safe_margin_y <= max_height:
                break
            else:
                font = ImageFont.truetype("arial.ttf", font.size - 2)
                total_text_height = sum(font.getbbox(line)[3] - font.getbbox(line)[1] for line in lines)
                safe_margin_y = position[1] + total_text_height

    text_position_y = position[1]

    for line in lines:
        _, _, text_width, text_height = draw.textbbox((0, 0), line, font=font)
        # Draw the text in the center
        draw.text(((position[0] - text_width) // 2, text_position_y), line, font=font, fill=font_color)

        text_position_y += text_height + margin  # Set the next y position for a new line

    return text_position_y, font.size


def draw_round_button(draw, text, font, position, text_padding, text_color="white", button_color="green"):
    """
    Draw a rounded button with text in the center.

    Args:
        draw (ImageDraw.Draw): The drawing context.
        text (str): The text to be displayed on the button.
        font (ImageFont.FreeTypeFont): The font to be used for the text.
        position (tuple): The position of the button.
        text_padding (int): The padding around the text.
        text_color (str): The color of the text (default is "white").
        button_color (str): The color of the button (default is "green").
    """
    # Calculate the text bbox
    text_bbox = draw.textbbox((0, 0), text, font=font)

    # Calculate the button size based on text size and padding
    button_size = (text_bbox[2] - text_bbox[0] + 2 * text_padding, text_bbox[3] - text_bbox[1] + 2 * text_padding)

    x, y = position
    width, height = button_size

    # Draw the filled rounded rectangle with rounded corners
    corner_radius = min(width, height) // 8  # Adjust this factor as needed

    draw.rectangle([x + corner_radius, y, x + width - corner_radius, y + height], fill=button_color)

    # Draw the text in the center of the button
    text_position = (
        x + (width - text_bbox[2]) // 2,
        y + (height - text_bbox[3]) // 2
    )

    draw.text(text_position, text, font=font, fill=text_color)