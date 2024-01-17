import numpy as np
from PIL import Image, ImageOps
from scipy.ndimage import binary_dilation


def extract_features_and_change_their_color(original_image, target_color, smooth_factor=0.5, dilation_radius=5):
    """
    Change the color of extracted features in an image.

    Args:
        original_image (PIL.Image.Image): The original image.
        target_color (tuple): The target color in RGB format.
        smooth_factor (float, optional): The interpolation factor between original and target color. Defaults to 0.5.
        dilation_radius (int, optional): The radius for dilating the feature mask. Defaults to 5.

    Returns:
        PIL.Image.Image: The resulting image with color-changed features.
    """
    # Convert the original image to a NumPy array
    image_array = np.array(original_image)

    # Extract features (for example, edges) - You can replace this with your feature extraction method
    # For this example, let's convert the image to grayscale and invert the colors
    features_array = 255 - np.array(ImageOps.grayscale(original_image))

    # Create a mask where features are present
    feature_mask = features_array > 0

    # Dilate the feature mask to include surrounding pixels
    dilated_feature_mask = binary_dilation(feature_mask, iterations=dilation_radius)

    # Smoothly interpolate between the original image and the target color for the features
    result_array = np.where(dilated_feature_mask[:, :, None],
                            (smooth_factor * np.array(target_color)).astype(np.uint8) +
                            ((1 - smooth_factor) * image_array).astype(np.uint8),
                            image_array)

    # Convert NumPy array back to an image
    result_image = Image.fromarray(result_array.astype(np.uint8))

    # Save or display the resulting image
    return result_image
