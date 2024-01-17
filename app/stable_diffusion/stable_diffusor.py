# Third-party libraries
import torch
from PIL import ImageColor
from diffusers import StableDiffusionImg2ImgPipeline

# Import helper functions
try:
    from .helpers import *
except ImportError:
    from helpers import *


class StableDiffusor:
    """
    A class for generating similar images by changing color features using the Stable Diffusion
    Image-to-Image transformation method.

    Attributes:
        pipe (StableDiffusionImg2ImgPipeline): The configured diffusion pipeline.

    Methods:
        __init__():
            Initializes a StableDiffusor object.

        create_pipeline():
            Creates and configures a StableDiffusionImg2ImgPipeline for image generation.

        generate_similar_image_by_color(base_image, positive_prompt, negative_prompt, hex_code='#008aed',
                                        smooth_factor=0.5, dilation_radius=5, strength=0.5,
                                        guidance_scale=7.5, steps=25) -> PIL.Image.Image:
            Generates a similar image by changing the color features of the base image.

            Args:
                base_image (PIL.Image.Image): The base image to be modified.
                positive_prompt (str): The positive prompt for image generation.
                negative_prompt (str): The negative prompt for image generation.
                hex_code (str): The hexadecimal color code applied to the base image.
                smooth_factor (float, optional): The interpolation factor between original and target color.
                dilation_radius (int, optional): The radius for dilating the feature mask.
                strength (float, optional): The strength parameter for the diffusion process.
                guidance_scale (float, optional): The scale parameter for guidance in the diffusion process.
                steps (int, optional): The number of steps in the diffusion process.

            Returns:
                PIL.Image.Image: The generated image with similar features.

            Notes:
                - The `extract_features_and_change_their_color` function is used internally to change color features.
                  For more details about its parameters, refer to its docstring.
    """

    def __init__(self):
        self.pipe = None

    def create_pipeline(self):
        """
        Create and configure a StableDiffusionImg2ImgPipeline for image generation.
        """
        # Specify the device for running the diffusion model
        device = "cuda"

        # Define the model ID or path for the Stable Diffusion model
        model_id_or_path = "prompthero/openjourney-v4"

        # Instantiate the StableDiffusionImg2ImgPipeline with the specified model and data type
        self.pipe = StableDiffusionImg2ImgPipeline.from_pretrained(model_id_or_path, torch_dtype=torch.float16)

        # Move the pipeline to the specified device (e.g., GPU)
        self.pipe = self.pipe.to(device)

    def generate_similar_image_by_color(self,
                                        base_image,
                                        positive_prompt,
                                        negative_prompt,
                                        hex_code='#008aed',
                                        smooth_factor=0.5,
                                        dilation_radius=5,
                                        strength=0.5,
                                        guidance_scale=7.5,
                                        steps=25) -> Image.Image:
        """
        Generate a similar image by changing the color features of the base image using the stable diffusion
        Image-to-Image transformation method.

        Args:
            base_image (PIL.Image.Image): The base image to be modified.
            positive_prompt (str): The positive prompt for image generation.
            negative_prompt (str): The negative prompt for image generation.
            hex_code (str): The hexadecimal color code which will be applied to the base image.
            smooth_factor (float, optional): The interpolation factor between original and target color.
            dilation_radius (int, optional): The radius for dilating the feature mask.
            strength (float, optional): The strength parameter for the diffusion process.
            guidance_scale (float, optional): The scale parameter for guidance in the diffusion process.
            steps (int, optional): The number of steps in the diffusion process.

        Returns:
            PIL.Image.Image: The generated image with similar features.

        Notes:
            - The `extract_features_and_change_their_color` function is used internally to change color features.
              For more details about its parameters, refer to its docstring.
        """
        # Convert the hexadecimal color code to RGB format
        rgb_color = ImageColor.getcolor(hex_code, "RGB")

        # Extract and change color features of the base image
        color_filtered_base_image = extract_features_and_change_their_color(original_image=base_image,
                                                                            target_color=rgb_color,
                                                                            smooth_factor=smooth_factor,
                                                                            dilation_radius=dilation_radius)

        # Create the transformation pipeline
        self.create_pipeline()

        # Generate the final output image by applying the stable diffusion process
        output_image = self.pipe(prompt=positive_prompt,
                                 negative_prompt=negative_prompt,
                                 image=color_filtered_base_image,
                                 strength=strength,
                                 guidance_scale=guidance_scale,
                                 steps=steps).images[0]

        return output_image


if __name__ == "__main__":
    # Create an instance of the StableDiffusor class
    stable_diffusor = StableDiffusor()

    # Open the sample image from the specified path
    image = Image.open("input.png")

    # Define positive and negative prompts for image generation
    positive_prompt = "generate similar image, keep context, UHD, 4K"
    negative_prompt = "science fiction features, unrealistic features, unrelated contents, " \
                      "text, words, logos, distortions in shapes, undesired features," \
                      "ugly, deformed, disfigured, poor details, bad anatomy"

    # Specify the target color using a hexadecimal code
    hex_code = '#b36a0b'

    # Generate a similar image by changing color features
    result_image = stable_diffusor.generate_similar_image_by_color(base_image=image,
                                                                   positive_prompt=positive_prompt,
                                                                   negative_prompt=negative_prompt,
                                                                   hex_code=hex_code)

    # Display the generated image
    result_image.show()

    # Save the generated image to the specified path in PNG format
    output_path = "output.png"
    result_image.save(output_path, format="PNG")
