from gradio_client import Client
import gradio as gr
import logging
import os
from PIL import Image
import uuid

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

if not os.path.exists("./temp"):
    os.makedirs("./temp")

# Constants

MAX_DIMENSION = 1280
MODEL_PATH = "models"
COLOUR_MODEL = "RGB"

STYLE_SHINKAI = "Makoto Shinkai"
STYLE_HOSODA = "Mamoru Hosoda"
STYLE_MIYAZAKI = "Hayao Miyazaki"
STYLE_KON = "Satoshi Kon"
DEFAULT_STYLE = STYLE_SHINKAI
STYLE_CHOICE_LIST = [STYLE_SHINKAI, STYLE_HOSODA, STYLE_MIYAZAKI, STYLE_KON]

client = Client("https://asach-animebackgroundgan.hf.space/", hf_token="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")

def inference(img, style):
    id  = str(uuid.uuid4())
    img.save( f"./temp/image_{id}_.jpg", format="JPEG")
    # Make request to Gradio app's API
    result = client.predict(f"./temp/image_{id}_.jpg", style, api_name="/predict")
    #delete temp file
    os.remove(f"./temp/image_{id}_.jpg")
    return Image.open(result)

# Gradio setup

title = "2 Gradio App"

examples = [
    ["examples/garden_in.jpg", STYLE_SHINKAI],
    ["examples/library_in.jpg", STYLE_KON],
]


gr.Interface(
    fn=inference,
    inputs=[
        gr.inputs.Image(
            type="pil",
            label="Input Photo (less than 1280px on both width and height)",
        ),
        gr.inputs.Dropdown(
            STYLE_CHOICE_LIST,
            type="value",
            default=DEFAULT_STYLE,
            label="Style",
        ),
    ],
    outputs=gr.outputs.Image(
        type="pil",
        label="Output Image",
    ),
    title=title,

    examples=examples,
    allow_flagging="never",
    allow_screenshot=False,
).launch(enable_queue=True)
