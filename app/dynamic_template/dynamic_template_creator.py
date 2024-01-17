try:
    from .helpers import *
except ImportError:
    from helpers import *


class DynamicTemplate:
    """
    A class for generating dynamic ad templates with a logo, base image, punchline text, and a call-to-action button.

    Attributes:
        result_image_size (tuple): The size (width, height) of the output image.
        logo_image_size (tuple): The size (width, height) of the logo image.
        template_width (int): The width of the template.
        template_height (int): The height of the template.
        logo_image_top_margin (int): The top margin for placing the logo.
        spacing_between_result_image_and_logo_image (int): Spacing between the result image and the logo image.
        font_name (str): The font name for punchline text and button text.
        font_size (int): The font size for punchline text.
        spacing_between_result_image_and_punchline_text (int): Spacing between the result image and punchline text.
        button_text_padding (int): Padding around the button text.
        spacing_between_punchline_text_and_button (int): Spacing between punchline text and the call-to-action button.

    Methods:
        __init__():
            Initializes a DynamicTemplate object with default values.

        generate_dynamic_ad_template(result_image, logo_image, punchline_text, punchline_text_color,
                                     button_text, button_text_color) -> Pillow.Image:
            Generates a dynamic ad template with a logo, base image, punchline text, and a call-to-action button.

            Args:
                result_image (Pillow.Image): Output image of stable_diffusor.generate_similar_image_by_color function.
                logo_image (Pillow.Image): Logo image.
                punchline_text (str): The punchline text.
                punchline_text_color (str): The color of the punchline text.
                button_text (str): The text on the call-to-action button.
                button_text_color (str): The color of the button text.

            Returns:
                Pillow.Image: The resulting template image.
    """

    def __init__(self):
        # Default values for template parameters
        self.result_image_size = (360, 360)
        self.logo_image_size = (128, 128)
        self.template_width = 720
        self.template_height = 720
        self.logo_image_top_margin = 10
        self.spacing_between_result_image_and_logo_image = 20
        self.font_name = "comicbd.ttf"
        self.font_size = 20
        self.spacing_between_result_image_and_punchline_text = 10
        self.punchline_text_spacing = 15
        self.punchline_text_maximum_height = int(self.template_height * 0.85)
        self.button_text_padding = 10
        self.spacing_between_punchline_text_and_button = 10

    def generate_dynamic_ad_template(self,
                                     result_image,
                                     logo_image,
                                     punchline_text,
                                     punchline_text_color,
                                     button_text,
                                     button_text_color):
        """
        Generate a dynamic ad template with a logo, base image, punchline text, and a call-to-action button.

        Args:
            result_image(Pillow.Image): Output image of stable_diffusor.generate_similar_image_by_color function.
            logo_image (Pillow.Image): Logo image.
            punchline_text (str): The punchline text.
            punchline_text_color (str): The color of the punchline text.
            button_text (str): The text on the call-to-action button.
            button_text_color (str): The color of the button text.

        Returns:
            Pillow.Image: The resulting template image.
        """

        # Load images
        result_img = resize_and_round_corners(result_image,
                                              self.result_image_size)

        logo_img = logo_image.resize(self.logo_image_size)

        # Create a blank template
        template = Image.new("RGB", (self.template_width, self.template_height), "white")
        draw = ImageDraw.Draw(template)

        # Paste logo at the top center
        logo_image_position = ((self.template_width - logo_img.width) // 2, self.logo_image_top_margin)
        template.paste(logo_img, logo_image_position)

        # Paste base image in the middle
        result_image_position = (
            (self.template_width - result_img.width) // 2,
            logo_image_position[1] + logo_img.height + self.spacing_between_result_image_and_logo_image
        )

        template.paste(result_img, result_image_position)

        # Draw punchline text in the middle
        punchline_font = ImageFont.truetype(self.font_name, self.font_size)

        _, _, text_width, text_height = draw.textbbox((0, 0), punchline_text, font=punchline_font)

        punchline_text_position = (self.template_width,
                                   result_img.height + result_image_position[
                                       1] + self.spacing_between_result_image_and_punchline_text)

        last_text_height, punchline_text_font_size = write_multiline_text(draw=draw,
                                                                          text=punchline_text,
                                                                          position=punchline_text_position,
                                                                          font=punchline_font,
                                                                          font_color=punchline_text_color,
                                                                          margin=self.punchline_text_spacing,
                                                                          max_height=self.punchline_text_maximum_height)

        # Draw button text at the bottom center
        button_font = ImageFont.truetype(self.font_name, punchline_text_font_size)
        _, _, button_width, button_height = draw.textbbox((0, 0), button_text, font=button_font)
        button_position = (
            (self.template_width - button_width - self.button_text_padding) // 2,
            last_text_height + self.spacing_between_punchline_text_and_button
        )

        draw_round_button(draw=draw,
                          text=button_text,
                          font=button_font,
                          position=button_position,
                          text_padding=self.button_text_padding,
                          text_color=button_text_color,
                          button_color=punchline_text_color)

        return template


if __name__ == "__main__":
    result_image = Image.open("../stable_diffusion/output.png")
    logo_image = Image.open("logo.png")

    dynamic_template_creator = DynamicTemplate()
    output_template = dynamic_template_creator.generate_dynamic_ad_template(result_image,
                                                                            logo_image,
                                                                            "Ai ad banners lead to higher conversions ratesxxxx",
                                                                            "#eb4034",
                                                                            "Call to action text here",
                                                                            "#0051ff")

    output_template.show()
    output_template.save("template_image.png")
