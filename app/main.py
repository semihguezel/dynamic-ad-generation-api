# Third-party libraries
import io
import uvicorn
import nest_asyncio
from PIL import Image
from pyngrok import conf
from pyngrok import ngrok
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, File, UploadFile, HTTPException

# Custom functions
from helpers import *
from stable_diffusion.stable_diffusor import StableDiffusor
from dynamic_template.dynamic_template_creator import DynamicTemplate

# Initiating a FastAPI instance sets the stage for crafting APIs with Python's efficiency.
app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)


@app.post("/ad_template_creator")
async def ad_template_creator(
        base_image: UploadFile = File(...),
        base_image_color: str = "",
        positive_prompt: str = "",
        negative_prompt: str = "",
        strength: float = 0.5,
        guidance_scale: float = 7.5,
        steps: int = 25,
        logo_image: UploadFile = File(...),
        punchline_text: str = "",
        punchline_text_color: str = "",
        button_text: str = "",
        button_text_color: str = "",
) -> FileResponse:
    """
    Create a dynamic ad template based on user inputs.

    Args:
        base_image (UploadFile): The main image for the template.
        base_image_color (str): The color code used for image manipulation.
        positive_prompt (str): The positive prompt for image generation.
        negative_prompt (str): The negative prompt for image generation.
        strength (float, optional): The strength parameter for the diffusion process (default is 0.5).
        guidance_scale (float, optional): The scale parameter for guidance in the diffusion process (default is 7.5).
        steps (int, optional): The number of steps in the diffusion process (default is 25).
        logo_image (UploadFile): The logo image to be included in the template.
        punchline_text (str): The punchline text to be displayed in the template.
        punchline_text_color (str): The color code for the punchline text.
        button_text (str): The text for the button in the template.
        button_text_color (str): The color code for the button text.

    Raises:
        HTTPException: If any validation fails or an internal server error occurs.

    Returns:
        FileResponse: The generated ad template file.
    """

    try:
        # Check if base_image_color is a valid hexadecimal color code
        if not is_valid_hex_color_code(base_image_color):
            raise HTTPException(status_code=422,
                                detail="Invalid base_image_color. Please provide a valid hexadecimal color code.")

        # Check if punchline_text_color is a valid hexadecimal color code
        if not is_valid_hex_color_code(punchline_text_color):
            raise HTTPException(status_code=422,
                                detail="Invalid punchline_text_color. Please provide a valid hexadecimal color code.")

        # Check if button_text_color is a valid hexadecimal color code
        if not is_valid_hex_color_code(button_text_color):
            raise HTTPException(status_code=422,
                                detail="Invalid button_text_color. Please provide a valid hexadecimal color code.")

        # Check if base_image is a valid image
        if not is_valid_image(base_image):
            raise HTTPException(status_code=422, detail="Invalid base_image. Please provide a valid image file.")

        # Check if logo_image is a valid image
        if not is_valid_image(logo_image):
            raise HTTPException(status_code=422, detail="Invalid logo_image. Please provide a valid image file.")

        # Check if text inputs are valid
        if not is_valid_text(punchline_text):
            raise HTTPException(status_code=422,
                                detail="Invalid punchline_text. Please provide a valid non-empty text.")

        if not is_valid_text(button_text):
            raise HTTPException(status_code=422, detail="Invalid button_text. Please provide a valid non-empty text.")

        # Read and process base image
        contents_base = await base_image.read()
        base_image_obj = Image.open(io.BytesIO(contents_base))

        # Read logo image
        contents_logo = await logo_image.read()
        logo_image_obj = Image.open(io.BytesIO(contents_logo))

        # Generate similar image using color
        stable_diffusor = StableDiffusor()
        result_image = stable_diffusor.generate_similar_image_by_color(base_image=base_image_obj,
                                                                       positive_prompt=positive_prompt,
                                                                       negative_prompt=negative_prompt,
                                                                       hex_code=base_image_color,
                                                                       strength=strength,
                                                                       guidance_scale=guidance_scale,
                                                                       steps=steps)

        # Create the ad template using user inputs
        dynamic_template_creator = DynamicTemplate()
        add_template = dynamic_template_creator.generate_dynamic_ad_template(
            result_image=result_image,
            logo_image=logo_image_obj,
            punchline_text=punchline_text,
            punchline_text_color=punchline_text_color,
            button_text=button_text,
            button_text_color=button_text_color,
        )

        # Create a temporary file path for the result image
        result_image_path = "output.png"

        # Save the result image
        add_template.save(result_image_path, format="PNG")

        # Return the temporary file to the user
        return FileResponse(result_image_path, media_type="image/png", filename="output.png")

    except HTTPException as http_exc:
        raise http_exc  # FastAPI HTTP exceptions are already well-formatted
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal Server Error. Please try again later.")


@app.get("/")
def read_root():
    """
    Endpoint for root path, returns a health check response.

    Returns:
        dict: A dictionary indicating the health check status.
    """
    return {"health_check": "OK"}


@app.get("/favicon.ico")
def get_favicon():
    """
    Endpoint for favicon.ico, returns a message indicating no favicon is available.

    Returns:
        dict: A dictionary with a message about the absence of a favicon.
    """
    return {"message": "No favicon"}


if __name__ == "__main__":
    conf.get_default().auth_token = "<insert_your_authtoken_here>"
    ngrok_tunnel = ngrok.connect(8087)
    print("Public URL:", ngrok_tunnel.public_url)
    nest_asyncio.apply()
    uvicorn.run(app, port=8087)
