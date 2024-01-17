
def is_valid_hex_color_code(color_code):
    """
    Check if the input string is a valid hexadecimal color code.

    Args:
        color_code (str): The input color code to be validated.

    Returns:
        bool: True if the color code is valid, False otherwise.
    """
    return color_code.startswith("#") and all(c in "0123456789ABCDEFabcdef" for c in color_code[1:])


def is_valid_image(file):
    """
    Check if the uploaded file is a valid image.

    Args:
        file (UploadFile): The uploaded file to be validated.

    Returns:
        bool: True if the file is a valid image, False otherwise.
    """
    try:
        file.read()
        return True
    except Exception:
        return False


def is_valid_text(text):
    """
    Check if the input text is valid (not empty, etc.).

    Args:
        text (str): The input text to be validated.

    Returns:
        bool: True if the text is valid, False otherwise.
    """
    return bool(text.strip())
